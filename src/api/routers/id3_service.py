from fastapi import APIRouter, UploadFile, HTTPException
from starlette import status

from src.api.middleware.custom_exceptions.WrongFileType import WrongFileType
from src.api.middleware.exceptions import exception_mapping
from src.service.id3.validation import check_input_file

router = APIRouter(
    prefix="/api/id3service", tags=["ID3 Service"]
)


@router.post("/uploadfile")
def upload_file(file: UploadFile):
    try:
        # input validation
        check_input_file(file)
        return {"message": "File uploaded successfully"}
    except WrongFileType as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
