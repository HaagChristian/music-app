import requests
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.settings.error_messages import DB_NO_RESULT_FOUND, FILE_CONVERSION_ERROR, UNSUPPORTED_FORMAT_ERROR
from src.settings.settings import REQUEST_TO_ENCODER_SERVICE
from sqlalchemy.orm import Session
from src.database.musicDB.db import get_db_music, commit_or_rollback_backup
from src.database.musicDB.db_crud import add_converted_file
from src.database.musicDB.db_crud import get_file_by_id


http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/encoderservice",
    tags=["Encoder Service"],
    dependencies=[Depends(http_bearer)]
)

# TODO: fix
@router.post("/convertfile")
@commit_or_rollback_backup
def convert_file(file_id: int, target_format: str, db: Session = Depends(get_db_music)):
    if target_format not in ["wav", "flac", "ogg"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=UNSUPPORTED_FORMAT_ERROR)

    file = get_file_by_id(db, file_id)
    if not file:
        raise NoResultFound(DB_NO_RESULT_FOUND)

    src_format = file.content_type.split('/')[-1]
    file_content = file.file.read()
    files = {'file': (file.filename, file_content, file.content_type)}
    data = {'src_format': src_format, 'target_format': target_format}

    response = requests.post(f"http://{REQUEST_TO_ENCODER_SERVICE}:8002/api/encoder/convert", files=files, data=data)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=FILE_CONVERSION_ERROR)

    converted_file = add_converted_file(db, file_id, response.content, target_format)

    return converted_file
