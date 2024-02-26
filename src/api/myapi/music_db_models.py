from pydantic import BaseModel, ConfigDict
from typing import Optional, List


class FileBase(BaseModel):
    file_data: bytes
    file_type: str
    file_name: str


class FileCreate(FileBase):
    pass


class File(FileBase):
    model_config = ConfigDict(from_attributes=True)
    file_id: int


class ConvertedFileBase(BaseModel):
    original_file_id: int
    file_type: str


class ConvertedFileCreate(ConvertedFileBase):
    pass


class ConvertedFile(ConvertedFileBase):
    model_config = ConfigDict(from_attributes=True)
    conversion_id: int


class ArtistBase(BaseModel):
    artist_name: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    model_config = ConfigDict(from_attributes=True)
    artist_id: int


class GenreBase(BaseModel):
    genre_name: str


class GenreCreate(GenreBase):
    pass


class Genre(GenreBase):
    model_config = ConfigDict(from_attributes=True)
    genre_id: int


class AlbumBase(BaseModel):
    album_name: str
    artist_id: int


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    model_config = ConfigDict(from_attributes=True)
    album_id: int


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
    model_config = ConfigDict(from_attributes=True)
    song_id: int


class SongArtistBase(BaseModel):
    song_id: int
    artist_id: int


class SongArtistCreate(SongArtistBase):
    pass


class SongArtist(SongArtistBase):
    model_config = ConfigDict(from_attributes=True)


class SongWithRelations(Song):
    model_config = ConfigDict(from_attributes=True)
    album: Optional[Album] = None
    genre: Optional[Genre] = None
    artists: List[Artist] = []


class FileDetailModel(File):
    model_config = ConfigDict(from_attributes=True)
    song: SongWithRelations


class SongWithRelationsAndFile(SongWithRelations):
    file: Optional[File] = None
