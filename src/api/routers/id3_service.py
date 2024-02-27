import logging

import requests
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.responses import Response

from src.api.middleware.custom_exceptions.MissingTitleFromMetadataError import MissingTitleFromMetadataError
from src.api.middleware.custom_exceptions.NoMetadataPassedError import NoMetadataPassedError
from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.metadata_model import MetadataResponse, MetadataToChangeRequest, MetadataId3Input, DBMetadata
from src.database.musicDB.db import get_db_music, commit_with_rollback_backup
from src.database.musicDB.db_crud import add_file_and_metadata, get_song_by_title, get_file_by_song_id
from src.service.helper import get_file_bytes, file_helper_with_temp_file
from src.service.id3.validation import check_input_file
from src.service.mapping.map_data import map_data_from_request_call
from src.service.mapping.map_db_data import input_mapping_from_change_metadata
from src.settings.error_messages import NO_METADATA_FOUND, METADATA_VALIDATION_ERROR, SONG_ALREADY_IN_DB, \
    DB_NO_RESULT_FOUND, UPDATE_METADATA_FROM_FILE
from src.settings.settings import REQUEST_TO_ID3_SERVICE

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/id3service", tags=["ID3 Service"],
    dependencies=[Depends(http_bearer)]
)


@router.post("/uploadfile", response_model=MetadataResponse, response_model_exclude_none=True)
@commit_with_rollback_backup
def upload_file(response: Response, request: Request,
                file: UploadFile = File(..., media_type="audio/mpeg", description="The mp3 file to upload"),
                db=Depends(get_db_music)):
    """
        Upload a file and get the metadata from it
        :param response: Response
        :param request: Request required for the middleware and commit_with_rollback_backup
        :param file: UploadFile
        :param db: Session

        :return: MetadataResponse
    """
    try:
        # input validation
        check_input_file(file)

        res = requests.post(f"http://{REQUEST_TO_ID3_SERVICE}:8001/api/metadata/get-data", files={'file': file.file})
        if res.status_code not in [200, 206]:
            if res.status_code == 422:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=NO_METADATA_FOUND)
            # error occurred during the request
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=METADATA_VALIDATION_ERROR)

        metadata = map_data_from_request_call(res)

        is_song_already_in_db = get_song_by_title(db=db, metadata=metadata)
        if is_song_already_in_db:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=SONG_ALREADY_IN_DB)

        add_file_and_metadata(db=db, file=get_file_bytes(file=file), metadata=metadata, file_name=file.filename)

        if res.status_code == 206:  # not all metadata are available in the file
            response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return metadata
    except (WrongFileType, MissingTitleFromMetadataError) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))


@router.post("/change-metadata")
@commit_with_rollback_backup
def change_metadata(request: Request, metadata_to_change: MetadataToChangeRequest, db=Depends(get_db_music)):
    """ Change the metadata of a file in the database and in the file itself """
    try:
        mapped_input_data: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)
        db_res = get_file_by_song_id(db=db, song_id=metadata_to_change.song_id)

        # no file found with specified file id
        if not db_res:
            raise NoResultFound(DB_NO_RESULT_FOUND)

        # create JSON String for the request to the id3 service because content can only be passed as JSON String
        # (passing file and content as form-data is not possible)
        body_metadata_req = {
            'metadata': f'{{"artist": "{mapped_input_data.artists}", "title": "{mapped_input_data.title}", '
                        f'"album": "{mapped_input_data.album}", "genre": "{mapped_input_data.genre}", '
                        f'"file_name": "{db_res.FILE_NAME}", "date": "{mapped_input_data.date}"}}'
        }

        res = requests.post(f"http://{REQUEST_TO_ID3_SERVICE}:8001/api/metadata/update-metadata",
                            files={'file': db_res.FILE_DATA},
                            data=body_metadata_req)

        if res.status_code != 200:
            logging.error(f'Error occurred while updating metadata: {res.text}')
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=UPDATE_METADATA_FROM_FILE)

        metadata_db = DBMetadata(artists=metadata_to_change.artists, title=mapped_input_data.title,
                                 album=mapped_input_data.album, genre=mapped_input_data.genre,
                                 song_id=metadata_to_change.song_id, date=metadata_to_change.date)

        file_helper_with_temp_file(db=db, res=res, metadata_db=metadata_db, filename=db_res.FILE_NAME)

        return Response(status_code=status.HTTP_200_OK, content="Metadata updated successfully")

    except (NoMetadataPassedError, NoResultFound) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
