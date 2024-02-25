import requests
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends, Request
from fastapi.security import HTTPBearer
from starlette import status
from starlette.responses import Response

from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.metadata_model import MetadataResponse, Artist
from src.database.musicDB.db import get_db_music, commit_with_rollback_backup
from src.database.musicDB.db_crud import add_file_and_metadata
from src.service.helper import get_file_bytes
from src.settings.error_messages import NO_METADATA_FOUND, METADATA_VALIDATION_ERROR
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
    try:
        # input validation
        # check_input_file(file) # TODO: wider auskommentieren sobald eine gute Testdatei da ist

        res = requests.post(f"http://{REQUEST_TO_ID3_SERVICE}:8001/api/metadata/get-data", files={'file': file.file})
        if res.status_code not in [200, 206]:
            if res.status_code == 422:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=NO_METADATA_FOUND)
            # error occurred during the request
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=METADATA_VALIDATION_ERROR)

        # map the data to the response model so that the response is independent of the underlying service
        list_of_artists = res.json().get('artists', [])
        artists_objects = [Artist(name=artist) for artist in list_of_artists]

        res_from_request = res.json()
        res_from_request['artists'] = artists_objects
        metadata = MetadataResponse(**res_from_request)

        add_file_and_metadata(db=db, file=get_file_bytes(file=file), metadata=metadata, file_name=file.filename)

        if res.status_code == 206:
            response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return metadata
    except WrongFileType as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
