import io
import requests
from fastapi import APIRouter, HTTPException, Depends, UploadFile, Request
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound

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

@router.post("/convertfile/{file_id}", response_model=ConvertedFile)
@commit_with_rollback_backup
def convert_file(request: Request, file_id: int, target_format: str, db: Session = Depends(get_db_music)):
    if target_format not in ["wav", "flac", "ogg"]:
        raise HTTPException(status_code=400, detail=UNSUPPORTED_FORMAT_ERROR)

    file = get_file_by_id(db, file_id)
    print(f"file:{file}")
    if not file:
        raise NoResultFound(DB_NO_RESULT_FOUND)

    src_format = file.FILE_TYPE
    file_content = io.BytesIO(file.FILE_DATA)
    print(f"file_content:{file_content}")
    upload_file = UploadFile(filename=file.FILE_NAME, file=file_content)
    #print(upload_file.file.read())
    files = {'file': ('file', upload_file.file.read(), upload_file.content_type)}
    print(f"files:{files}")
    data = {'src_format': src_format, 'target_format': target_format}
    print(f"data: {data}")

    res = requests.post(f"http://{REQUEST_TO_ENCODER_SERVICE}:8002/api/encoder/convert", files=files, data=data)
    if res.status_code != 200:
        raise HTTPException(status_code=res.status_code, detail=FILE_CONVERSION_ERROR)

    converted_data = map_converted_data_from_request_call(res)
    print(f"converted_data:{converted_data}")

    converted_file = handle_conversion_response(converted_data, file_id, db)

    return converted_file
