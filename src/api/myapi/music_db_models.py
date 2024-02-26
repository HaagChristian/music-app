from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class FileBase(BaseModel):
    file_data: bytes
    file_type: str
    file_name: str


class FileCreate(FileBase):
    pass


class File(FileBase):
    file_id: int
    class Config:
        from_attributes = True


class ConvertedFileBase(BaseModel):
    original_file_id: int
    file_type: str


class ConvertedFileCreate(ConvertedFileBase):
    pass


class ConvertedFile(ConvertedFileBase):
    conversion_id: int
    class Config:
        from_attributes = True


class ArtistBase(BaseModel):
    artist_name: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    artist_id: int
    class Config:
        from_attributes = True


class GenreBase(BaseModel):
    genre_name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    genre_id: int
    class Config:
        from_attributes = True


class AlbumBase(BaseModel):
    album_name: str
    artist_id: int


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    album_id: int
    class Config:
        from_attributes = True


class SongBase(BaseModel):
    album_id: int
    genre_id: int
    file_id: int
    duration: Optional[int] = None
    title: str
    release_date: Optional[str] = None


class SongCreate(SongBase):
    pass


class Song(SongBase):
    song_id: int
    class Config:
        from_attributes = True


class SongArtistBase(BaseModel):
    song_id: int
    artist_id: int


class SongArtistCreate(SongArtistBase):
    pass


class SongArtist(SongArtistBase):
    class Config:
        from_attributes = True


class SongWithRelations(Song):
    album: Optional[Album] = None
    genre: Optional[Genre] = None
    artists: List[Artist] = []
    class Config:
        from_attributes = True


class FileDetailModel(File):
    song: SongWithRelations
    class Config:
        from_attributes = True



class SongWithRelationsAndFile(SongWithRelations):
    file: Optional[File] = None
