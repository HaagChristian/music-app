from typing import Optional

from pydantic import BaseModel


class MetadataResponse(BaseModel):
    title: Optional[str] = None
    artist: Optional[str] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    failed_tags: list = []
