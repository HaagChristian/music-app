import requests
from fastapi import APIRouter, UploadFile, HTTPException, File, Depends
from fastapi.security import HTTPBearer
from starlette import status
from starlette.responses import Response

from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.metadata_model import MetadataResponse
from src.service.id3.validation import check_input_file
from src.settings.error_messages import NO_METADATA_FOUND, METADATA_VALIDATION_ERROR

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/id3service", tags=["ID3 Service"],
    dependencies=[Depends(http_bearer)]
)


@router.post("/uploadfile", response_model=MetadataResponse, response_model_exclude_none=True)
def upload_file(response: Response,
                file: UploadFile = File(..., media_type="audio/mpeg", description="The mp3 file to upload")):
    try:
        # input validation
        check_input_file(file)

        res = requests.post("http://127.0.0.1:3000/api/metadata/get-data", files={'file': (file.filename, file.file)})
        if res.status_code not in [200, 206]:
            if res.status_code == 422:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=NO_METADATA_FOUND)
            # error occurred during the request
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=METADATA_VALIDATION_ERROR)

        # map the data to the response model so that the response is independent of the underlying service
        metadata = MetadataResponse(**res.json())

        # TODO safe response to db
        if res.status_code == 206:
            response.status_code = status.HTTP_206_PARTIAL_CONTENT
        return metadata
    except WrongFileType as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
