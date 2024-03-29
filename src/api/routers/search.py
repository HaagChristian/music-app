from typing import List, Dict

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.music_db_models import SongWithRelations
from src.api.myapi.search_model import SearchCriteria
from src.database.music_db.db import get_db_music
from src.database.music_db.db_search import *
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
    try:
        criteria_dict = fetch_all_search_criteria(db)
        if not criteria_dict:
            raise NoResultFound(DB_NO_RESULT_FOUND)
        return criteria_dict
    except NoResultFound as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))


@router.post("/search/combined", response_model=List[SongWithRelations], response_model_exclude_none=True)
def search_combined(criteria: SearchCriteria, db: Session = Depends(get_db_music)):
    try:
        songs = search_songs_combined(db, criteria.title, criteria.genre_name, criteria.artist_name,
                                      criteria.album_name)
        if not songs:
            raise NoResultFound(DB_NO_RESULT_FOUND)

        songs_with_rel: List[SongWithRelations] = []
        for song in songs:
            songs_with_rel.append(map_song_with_rel_to_model(song))
        return songs_with_rel
    except (ValueError, NoResultFound) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
