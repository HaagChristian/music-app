from typing import Optional, List

from pydantic import BaseModel


class MetadataResponse(BaseModel):
    title: Optional[str] = None
    artists: Optional[List[str]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
    failed_tags: Optional[List[str]] = None


class Artist(BaseModel):
    name: str


class MetadataFromSearch(BaseModel):
    title: Optional[str] = None
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
