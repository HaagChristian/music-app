from typing import Optional

from pydantic import BaseModel


class SearchCriteria(BaseModel):
    title: Optional[str] = None
    genre_name: Optional[str] = None
    artist_name: Optional[str] = None
    album_name: Optional[str] = None
