from pydantic import BaseModel, Field
from typing import Optional, List


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


class ConvertedFile(ConvertedFileBase):
    conversion_id: int
    class Config:
        from_attributes = True

class ConversionResponse(BaseModel):
    file_type: str
    file_data: str

class ArtistBase(BaseModel):
    artist_name: str


class Artist(ArtistBase):
    artist_id: int
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

class SimpleSong(BaseModel):
    song_id: int
    title: Optional[str] = None
    duration: Optional[float] = None
    release_date: Optional[str] = None

    class Config:
        from_attributes = True


class SongBase(BaseModel):
    album_id: int
    genre_id: int
    file_id: int
    duration: Optional[int] = None
    title: str
    release_date: Optional[str] = None



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
    album: Optional[Album] = None
    genre: Optional[Genre] = None
    artists: List[Artist] = []
    class Config:
        from_attributes = True


class SongWithRelationsAndFile(SongWithRelations):
    file: Optional[File] = None
