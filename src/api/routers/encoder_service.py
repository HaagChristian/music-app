import requests
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.middleware.custom_exceptions.unsupported_format_error import UnsupportedFormatError
from src.api.middleware.exceptions import exception_mapping
from src.service.mapping.map_data import map_converted_data_from_request_call
from src.settings.error_messages import DB_NO_RESULT_FOUND, FILE_CONVERSION_ERROR, UNSUPPORTED_FORMAT_ERROR
from src.settings.settings import REQUEST_TO_ENCODER_SERVICE
from sqlalchemy.orm import Session
from src.database.musicDB.db import get_db_music, commit_with_rollback_backup
from src.database.musicDB.db_crud import handle_conversion_response
from src.database.musicDB.db_crud import get_file_by_id
from src.api.myapi.music_db_models import ConvertedFile

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/encoderservice",
    tags=["Encoder Service"],
    dependencies=[Depends(http_bearer)]
)


@router.post("/convertfile/{file_id}")
@commit_with_rollback_backup
def convert_file(request: Request, file_id: int, target_format: str, db: Session = Depends(get_db_music)):
    """
    Convert a file to a different format and return the converted file
    """
    try:
        if target_format not in ["wav", "flac", "ogg"]:
            raise UnsupportedFormatError(UNSUPPORTED_FORMAT_ERROR)

        file = get_file_by_id(db, file_id)
        if not file:
            raise NoResultFound(DB_NO_RESULT_FOUND)

        src_format = file.FILE_TYPE

        data = {'input_model': f'{{"src_format": "{src_format}", "target_format": "{target_format}"}}'}

        res = requests.post(f"http://{REQUEST_TO_ENCODER_SERVICE}:8002/api/encoder/convert",
                            files={'file': file.FILE_DATA}, data=data)
        if res.status_code != 200:
            if res.status_code == 422:
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=res.json().get('detail'))
            raise HTTPException(status_code=res.status_code, detail=FILE_CONVERSION_ERROR)

        converted_data = map_converted_data_from_request_call(res)

        converted_file = handle_conversion_response(converted_data, file_id, file.FILE_NAME, db)

        return converted_file
    except (NoResultFound, UnsupportedFormatError) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
