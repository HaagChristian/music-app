from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database.musicDB.db import get_db_music
from src.api.myapi.music_db_models import FileDetailModel, Song, File, SongWithRelationsAndFile
from src.database.musicDB.db_crud import get_file_and_song_by_id, get_song_by_id, get_file_by_id, get_file_by_song_id, \
    get_song_and_file_by_song_id
from src.service.mapping.map_db_data import file_obj_to_model, song_and_file_obj_to_model
from src.settings.error_messages import NO_DB_RESULT_FOUND


http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/crud", tags=["CRUD Operations"],
    dependencies=[Depends(http_bearer)]
)


@router.get("/file/{file_id}", response_model=File)
def get_file(file_id: int, db: Session = Depends(get_db_music)):
    file = get_file_by_id(db, file_id)
    if not file:
        raise NoResultFound(NO_DB_RESULT_FOUND)
    return file


@router.get("/file/{song_id}", response_model=File)
def get_file_by_song_id(song_id: int, db: Session = Depends(get_db_music)):
    file = get_file_by_song_id(db, song_id)
    if not file:
        raise NoResultFound(NO_DB_RESULT_FOUND)
    return file


@router.get("/song/{song_id}", response_model=Song)
def get_song(song_id: int, db: Session = Depends(get_db_music)):
    song = get_song_by_id(db, song_id)
    if not song:
        raise NoResultFound(NO_DB_RESULT_FOUND)
    return song


"""returns song with file and relations accessed by file_id"""
@router.get("/file_and_song/{file_id}", response_model=FileDetailModel)
def get_file_and_song(file_id: int, db: Session = Depends(get_db_music)):
    file_obj = get_file_and_song_by_id(db, file_id)
    if not file_obj:
        raise NoResultFound(NO_DB_RESULT_FOUND)

    return file_obj_to_model(file_obj)


"""returns song with file and relations accessed by song_id"""
@router.get("/song_and_file/{song_id}", response_model=SongWithRelationsAndFile)
def get_song_and_file(song_id: int, db: Session = Depends(get_db_music)):
    song_obj = get_song_and_file_by_song_id(db, song_id)
    if not song_obj:
        raise NoResultFound(NO_DB_RESULT_FOUND)

    return song_and_file_obj_to_model(song_obj)


