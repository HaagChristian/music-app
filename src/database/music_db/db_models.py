from typing import List

from sqlalchemy import String, ForeignKey, Integer, LargeBinary, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref

from src.database.music_db.db import Base


class Artist(Base):
    __tablename__ = 'artists'

    ARTIST_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ARTIST_NAME: Mapped[str] = mapped_column(String(100))

    song: Mapped['SongArtist'] = relationship(back_populates="artist", overlaps='cycle')


class Album(Base):
    __tablename__ = 'albums'

    ALBUM_ID: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    ALBUM_NAME: Mapped[str] = mapped_column(String(100))

    song: Mapped['Song'] = relationship(back_populates="album")


class SongArtist(Base):
    __tablename__ = 'songs_artists'

    SONG_ID: Mapped[int] = mapped_column(Integer, ForeignKey('songs.SONG_ID'), primary_key=True, nullable=False,
                                         index=True)
    ARTIST_ID: Mapped[int] = mapped_column(Integer, ForeignKey('artists.ARTIST_ID'), primary_key=True, nullable=False,
                                           index=True)

    song: Mapped['Song'] = relationship(backref=backref('cycle',
                                                        cascade='save-update, merge, '
                                                                'delete, delete-orphan'))
    artist: Mapped['Artist'] = relationship(backref=backref('cycle',
                                                            cascade='save-update, merge, '
                                                                    'delete, delete-orphan'))


class ConvertedFile(Base):
    __tablename__ = 'converted_files'

    CONVERSION_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    ORIGINAL_FILE_ID: Mapped[int] = mapped_column(Integer, ForeignKey('files.FILE_ID'), nullable=False, index=True)
    FILE_DATA: Mapped[LargeBinary] = mapped_column(LargeBinary)
    FILE_TYPE: Mapped[str] = mapped_column(Enum('wav', 'flac', 'ogg'))
    FILE_NAME: Mapped[str] = mapped_column(String(100))

    file: Mapped['File'] = relationship(back_populates="converted_file")


class File(Base):
    __tablename__ = 'files'

    FILE_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    FILE_DATA: Mapped[LargeBinary] = mapped_column(LargeBinary)
    FILE_TYPE: Mapped[str] = mapped_column(Enum('mp3'))
    FILE_NAME: Mapped[str] = mapped_column(String(100))

    converted_file: Mapped['ConvertedFile'] = relationship(back_populates="file")
    song: Mapped['Song'] = relationship(back_populates="file")


class Genre(Base):
    __tablename__ = 'genres'

    GENRE_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    GENRE_NAME: Mapped[str] = mapped_column(String(100))

    song: Mapped['Song'] = relationship(back_populates="genre")


class Song(Base):
    __tablename__ = 'songs'

    SONG_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    ALBUM_ID: Mapped[int] = mapped_column(Integer, ForeignKey('albums.ALBUM_ID'), nullable=False)
    GENRE_ID: Mapped[int] = mapped_column(Integer, ForeignKey('genres.GENRE_ID'), nullable=False)
    FILE_ID: Mapped[int] = mapped_column(Integer, ForeignKey('files.FILE_ID'), nullable=False)
    DURATION: Mapped[int] = mapped_column(Integer)
    TITLE: Mapped[str] = mapped_column(String(100))
    RELEASE_DATE: Mapped[Date] = mapped_column(Date)

    artist: Mapped[List['SongArtist']] = relationship(back_populates="song", overlaps='cycle')
    file: Mapped['File'] = relationship(back_populates="song")
    album: Mapped['Album'] = relationship(back_populates="song")
    genre: Mapped['Genre'] = relationship(back_populates="song")
