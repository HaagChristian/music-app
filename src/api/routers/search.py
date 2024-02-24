from typing import List

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.api.myapi.music_db_models import SongWithRelations
from src.database.musicDB.db import get_db_music
from src.database.musicDB.db_search import *
from src.service.mapping.map_db_data import song_obj_to_model

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/search",
    tags=["Search Songs"],
    dependencies=[Depends(http_bearer)]
)

"""endpoints for simple search"""
''''
@router.get("/search/song_by_title", response_model=List[Song])
def search_song_by_title(title: str, db: Session = Depends(get_db_music)):
    songs = search_song_by_title(db, title)
    return songs


@router.get("/search/song_by_genre", response_model=List[Song])
def search_song_by_genre(genre_name: str, db: Session = Depends(get_db_music)):
    songs = search_songs_by_genre(db, genre_name)
    return songs


@router.get("/search/song_by_artist", response_model=List[Song])
def search_song_by_artist(artist_name: str, db: Session = Depends(get_db_music)):
    songs = search_songs_by_artist(db, artist_name)
    return songs


@router.get("/search/song_by_album", response_model=List[Song])
def search_song_by_album(album_name: str, db: Session = Depends(get_db_music)):
    songs = search_songs_by_album(db, album_name)
    return songs


@router.get("/search/combined", response_model=List[Song])
def search_combined(db: Session = Depends(get_db_music), title: str = None, genre_name: str = None,
                    artist_name: str = None, album_name: str = None):
    songs = search_songs_combined(db, title, genre_name, artist_name, album_name)
    return songs
'''

"""endpoints for songs with relations"""

@router.get("/search/song_by_title", response_model=List[SongWithRelations])
def search_song_by_title(title: str, db: Session = Depends(get_db_music)):
    songs = search_song_by_title(db, title)
    songs_with_rel = [song_obj_to_model(song) for song in songs]
    return songs_with_rel


@router.get("/search/song_by_genre", response_model=List[SongWithRelations])
def search_song_by_genre(genre_name: str, db: Session = Depends(get_db_music)):
    songs = search_songs_by_genre(db, genre_name)
    songs_with_rel = [song_obj_to_model(song) for song in songs]
    return songs_with_rel


@router.get("/search/song_by_artist", response_model=List[SongWithRelations])
def search_song_by_artist(artist_name: str, db: Session = Depends(get_db_music)):
    songs = search_songs_by_artist(db, artist_name)
    songs_with_rel = [song_obj_to_model(song) for song in songs]
    return songs_with_rel


@router.get("/search/song_by_album", response_model=List[SongWithRelations])
def search_song_by_album(album_name: str, db: Session = Depends(get_db_music)):
    songs = search_songs_by_album(db, album_name)
    songs_with_rel = [song_obj_to_model(song) for song in songs]
    return songs_with_rel


@router.get("/search/combined", response_model=List[SongWithRelations])
def search_combined(db: Session = Depends(get_db_music), title: str = None, genre_name: str = None,
                    artist_name: str = None, album_name: str = None):
    songs = search_songs_combined(db, title, genre_name, artist_name, album_name)
    songs_with_rel = [song_obj_to_model(song) for song in songs]
    return songs_with_rel

