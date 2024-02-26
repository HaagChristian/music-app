from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.security import HTTPBearer
from starlette import status

from src.api.myapi.metadata_model import MetadataFromSearch
from src.database.musicDB.db import get_db_music
from src.database.musicDB.db_search import search_for_title_and_artist
from src.service.mapping.map_db_data import map_search_db_data
from src.settings.error_messages import MISSING_DATA, DB_NO_RESULT_FOUND

http_bearer = HTTPBearer()

router = APIRouter(
    prefix="/api/data", tags=["Edit metadata"],
    dependencies=[Depends(http_bearer)]
)


@router.get("/search", response_model=List[MetadataFromSearch], response_model_exclude_none=True)
def search(title: str = Query(default=None, description='Title of the song'),
           artist: str = Query(default=None, description='Artist of the song'), db=Depends(get_db_music)):
    if not title and not artist:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=MISSING_DATA)

    # change for like search in db
    if title:
        title = "%{}%".format(title)

    res = search_for_title_and_artist(db=db, title=title, artist=artist)

    mapped_output: List[MetadataFromSearch] = map_search_db_data(res)
    if not mapped_output:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=DB_NO_RESULT_FOUND)

    return mapped_output


