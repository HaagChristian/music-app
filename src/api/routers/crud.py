from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from starlette import status

from src.api.middleware.exceptions import exception_mapping
from src.api.middleware.file_operations import create_and_return_file
from src.database.musicDB.db import get_db_music
from src.database.musicDB.db_crud import get_file_by_id, get_file_by_song_id, delete_song_and_file_by_song_id
from src.settings.error_messages import DB_NO_RESULT_FOUND

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/crud", tags=["CRUD Operations"],
    dependencies=[Depends(http_bearer)]
)


# TODO: einen von beiden File endpoints löschen
@router.get("/file/{file_id}")
def get_file(file_id: int, db: Session = Depends(get_db_music)):
    try:
        file_obj = get_file_by_id(db, file_id)
        if not file_obj:
            raise NoResultFound(DB_NO_RESULT_FOUND)
        return create_and_return_file(file_obj)
    except NoResultFound as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))


@router.get("/file/{song_id}")
def get_file_by_song(song_id: int, db: Session = Depends(get_db_music)):
    try:
        file_obj = get_file_by_song_id(db, song_id)
        if not file_obj:
            raise NoResultFound(DB_NO_RESULT_FOUND)
        return create_and_return_file(file_obj)
    except NoResultFound as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))


@router.delete("/delete_song_and_file/{song_id}")
def delete_song_and_file(song_id: int, db: Session = Depends(get_db_music)):
    try:
        delete_song_and_file_by_song_id(db, song_id)
        return {"message": "Song and associated file successfully deleted."}
    except NoResultFound as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
