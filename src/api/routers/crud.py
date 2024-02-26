from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from src.database.musicDB.db import get_db_music
from src.api.myapi.music_db_models import Song, File, SongWithRelationsAndFile, SimpleSong, SimpleFile
from src.database.musicDB.db_crud import get_song_by_id, get_file_by_id, get_file_by_song_id, \
    get_song_and_file_by_song_id
from src.service.mapping.map_db_data import song_and_file_obj_to_model
from src.settings.error_messages import DB_NO_RESULT_FOUND


http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/crud", tags=["CRUD Operations"],
    dependencies=[Depends(http_bearer)]
)

# TODO: fix all endpoints
@router.get("/simplefile/{file_id}", response_model=SimpleFile)
def get_file(file_id: int, db: Session = Depends(get_db_music)):
    file = get_file_by_id(db, file_id)
    if not file:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    simple_file = SimpleFile(
        file_id=file.FILE_ID,
        file_data=file.FILE_DATA,
        file_type=file.FILE_TYPE,
        file_name=file.FILE_NAME
    )
    return simple_file


@router.get("/file/{song_id}", response_model=File)
def get_file_by_song_id(song_id: int, db: Session = Depends(get_db_music)):
    file = get_file_by_song_id(db, song_id)
    if not file:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    return file


@router.get("/song/{song_id}", response_model=Song)
def get_song(song_id: int, db: Session = Depends(get_db_music)):
    song = get_song_by_id(db, song_id)
    if not song:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    return song

@router.get("/simplesong/{song_id}", response_model=SimpleSong)
def get_simple_song(song_id: int, db: Session = Depends(get_db_music)):
    song = get_song_by_id(db, song_id)
    if not song:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    simple_song = SimpleSong(
        song_id=song.SONG_ID,
        title=song.TITLE,
        duration=song.DURATION,
        release_date=song.RELEASE_DATE.strftime("%Y-%m-%d") if song.RELEASE_DATE else None
    )
    return simple_song


"""returns song with file and relations accessed by song_id"""
@router.get("/song_and_file/{song_id}", response_model=SongWithRelationsAndFile)
def get_song_and_file(song_id: int, db: Session = Depends(get_db_music)):
    song_obj = get_song_and_file_by_song_id(db, song_id)
    if not song_obj:
        raise NoResultFound(DB_NO_RESULT_FOUND)

    return song_and_file_obj_to_model(song_obj)


