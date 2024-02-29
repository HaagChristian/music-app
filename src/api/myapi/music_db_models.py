from typing import Optional, List, Union
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from src.api.myapi.metadata_model import Artist
from src.settings.error_messages import INVALID_YEAR


class FileBase(BaseModel):
    file_data: bytes
    file_type: str
    file_name: str


class File(FileBase):
    file_id: int

    class Config:
        from_attributes = True


class ConvertedFileBase(BaseModel):
    original_file_id: int
    file_data: bytes
    file_type: str
    file_name: str


class ConvertedFile(ConvertedFileBase):
    conversion_id: int

    class Config:
        from_attributes = True


class ConversionResponse(BaseModel):
    file_type: str
    file_data: bytes


class ArtistBase(Artist):
    id: int

    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    genre_name: str


class Genre(GenreBase):
    genre_id: int

    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    album_name: str


class Album(AlbumBase):
    album_id: int

    class Config:
        from_attributes = True


class SongBase(BaseModel):
    file_id: int
    duration: Optional[float] = None
    title: Optional[str] = None
    release_date: Optional[Union[int]] = Field(None, description='Date is only provided as year')


class Song(SongBase):
    song_id: int

    class Config:
        from_attributes = True


class SongArtistBase(BaseModel):
    song_id: int
    artist_id: int


class SongArtist(SongArtistBase):
    class Config:
        from_attributes = True


class SongWithRelations(Song):
    album: Optional[str] = None
    genre: Optional[str] = None
    artist: Optional[List[ArtistBase]] = None

    class Config:
        from_attributes = True
