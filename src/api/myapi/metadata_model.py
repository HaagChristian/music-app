from typing import Optional, List

from pydantic import BaseModel, Field


class Artist(BaseModel):
    name: str


class MetadataResponse(BaseModel):
    title: Optional[str] = None
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
    failed_tags: Optional[List[str]] = Field(None,
                                             description='List of metadata keys which are not in the metadata of the file')


class MetadataFromSearch(BaseModel):
    title: Optional[str] = None
    artists: Optional[List[Artist]] = None
    album: Optional[str] = None
    genre: Optional[str] = None
    date: Optional[str] = None
    duration: Optional[float] = None
