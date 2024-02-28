from typing import List, Dict

from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from src.api.myapi.music_db_models import SongWithRelations
from src.api.myapi.search_models import SearchCriteria
from src.database.musicDB.db import get_db_music
from src.database.musicDB.db_search import *
from src.service.mapping.map_db_data import map_song_with_rel_to_model
from src.settings.error_messages import DB_NO_RESULT_FOUND

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/search",
    tags=["Search Songs"],
    dependencies=[Depends(http_bearer)]
)


@router.get("/search/all_criteria", response_model=Dict[str, List[str]])
def get_all_search_criteria(db: Session = Depends(get_db_music)):
    criteria_dict = fetch_all_search_criteria(db)
    if not criteria_dict:
        raise NoResultFound(DB_NO_RESULT_FOUND)
    return criteria_dict


@router.post("/search/combined", response_model=List[SongWithRelations], response_model_exclude_none=True)
def search_combined(criteria: SearchCriteria, db: Session = Depends(get_db_music)):
    songs = search_songs_combined(db, criteria.title, criteria.genre_name, criteria.artist_name, criteria.album_name)
    songs_with_rel: List[SongWithRelations] = [map_song_with_rel_to_model(song) for song in songs]
    return songs_with_rel
