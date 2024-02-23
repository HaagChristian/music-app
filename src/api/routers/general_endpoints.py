from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.requests import Request

from src.api.middleware.custom_exceptions.NoMetadataPassedError import NoMetadataPassedError
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.metadata_model import MetadataFromSearch, MetadataToChange, MetadataId3Input, DBMetadata
from src.database.musicDB.db import get_db_music, commit_with_rollback_backup
from src.database.musicDB.db_queries import search_for_title_and_artist, get_file_by_id, update_file_and_metadata
from src.service.mapping.map_db_data import map_search_db_data, input_mapping_from_change_metadata
from src.settings.error_messages import MISSING_DATA, DB_NO_RESULT_FOUND

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/data", tags=["Edit metadata"],
    dependencies=[Depends(http_bearer)]
)


@router.get("/search", response_model=List[MetadataFromSearch], response_model_exclude_none=True)
def search(title: str = Query(default=None, description='Title of the song'),
           artist: str = Query(default=None, description='Artist of the song'), db=Depends(get_db_music)):
    if not title and not artist:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=MISSING_DATA)

    # change for like search in db
    if title:
        title = "%{}%".format(title)

    res = search_for_title_and_artist(db=db, title=title, artist=artist)

    mapped_output: List[MetadataFromSearch] = map_search_db_data(res)
    if not mapped_output:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DB_NO_RESULT_FOUND)

    return mapped_output


@router.post("/change-metadata")
@commit_with_rollback_backup
def change_metadata(request: Request, metadata_to_change: MetadataToChange, db=Depends(get_db_music)):
    try:
        mapped_input_data: MetadataId3Input = input_mapping_from_change_metadata(metadata_to_change)
        db_res = get_file_by_id(db=db, file_id=metadata_to_change.file_id)

        # no file found with specified file id
        if not db_res:
            raise NoResultFound(DB_NO_RESULT_FOUND)

        body_metadata_req = {
            'metadata': f'{{"artist": "{mapped_input_data.artists}", "title": "{mapped_input_data.title}", '
                        f'"album": "{mapped_input_data.album}", "genre": "{mapped_input_data.genre}", '
                        f'"file_name": "{db_res.FILE_NAME}"}}'
        }

        # res = requests.post(f"http://{REQUEST_TO_ID3_SERVICE}:8001/api/metadata/update-metadata",
        #                     files={'file': db_res.FILE_DATA},
        #                     data=body_metadata_req,
        #                     )
        res = 'a'
        metadata_db = DBMetadata(artists=mapped_input_data.artists, title=mapped_input_data.title,
                                 album=mapped_input_data.album, genre=mapped_input_data.genre,
                                 file_id=metadata_to_change.file_id)
        update_file_and_metadata(db=db, file=res, metadata=metadata_db)

        return {"message": "Hello World"}

    except (NoMetadataPassedError, NoResultFound) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
