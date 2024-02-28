import tempfile

from starlette.background import BackgroundTask
from starlette.responses import FileResponse
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.database.musicDB.db import get_db_music
from src.api.myapi.music_db_models import SongWithRelationsAndFile, SimpleSong, SongWithRelations
from src.database.musicDB.db_crud import get_song_by_id, get_file_by_id, get_file_by_song_id, \
    get_song_and_file_by_song_id, get_simple_song_by_id, delete_song_and_file_by_song_id
from src.service.mapping.map_db_data import map_simple_song_to_model, map_song_with_rel_and_file_to_model, map_song_with_rel_to_model
from src.settings.error_messages import DB_NO_RESULT_FOUND
from src.api.middleware.cleanup import cleanup


http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/crud", tags=["CRUD Operations"],
    dependencies=[Depends(http_bearer)]
)


@router.get("/file/{file_id}")
def get_file(file_id: int, db: Session = Depends(get_db_music)):
    file_obj = get_file_by_id(db, file_id)
    if not file_obj:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(file_obj.FILE_DATA)
        return FileResponse(temp_file_path, background=BackgroundTask(cleanup, temp_file_path=temp_file_path, temp_file=temp_file))


@router.get("/file/{song_id}")
def get_file_by_song(song_id: int, db: Session = Depends(get_db_music)):
    file_obj = get_file_by_song_id(db, song_id)
    if not file_obj:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file_path = temp_file.name
        temp_file.write(file_obj.FILE_DATA)
        return FileResponse(temp_file_path, background=BackgroundTask(cleanup, temp_file_path=temp_file_path, temp_file=temp_file))


@router.get("/song/{song_id}", response_model=SongWithRelations)
def get_song_with_rel(song_id: int, db: Session = Depends(get_db_music)):
    song_obj = get_song_by_id(db, song_id)
    if not song_obj:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    song_with_rel: SongWithRelations = map_song_with_rel_to_model(song_obj)
    return song_with_rel


# TODO: think about Song pydantic models
@router.get("/simplesong/{song_id}", response_model=SimpleSong)
def get_simple_song(song_id: int, db: Session = Depends(get_db_music)):
    song_obj = get_simple_song_by_id(db, song_id)
    if not song_obj:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    simple_song: SimpleSong = map_simple_song_to_model(song_obj)
    return simple_song


@router.get("/song_and_file/{song_id}", response_model=SongWithRelationsAndFile)
def get_song_and_file(song_id: int, db: Session = Depends(get_db_music)):
    """
    returns song with file and relations accessed by song_id
    """
    song_obj = get_song_and_file_by_song_id(db, song_id)
    if not song_obj:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    song_with_rel_and_file: SongWithRelationsAndFile = map_song_with_rel_and_file_to_model(song_obj)
    return song_with_rel_and_file


@router.delete("/delete_song_and_file/{song_id}")
def delete_song_and_file(song_id: int, db: Session = Depends(get_db_music)):
    if delete_song_and_file_by_song_id(db, song_id):
        return {"message": "Song and associated file successfully deleted."}
    raise NoResultFound(DB_NO_RESULT_FOUND)
