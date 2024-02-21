from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database.musicDB.db import Base


class Song(Base):
    __tablename__ = 'songs'

    SONG_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    ALBUM_ID: Mapped[int] = mapped_column(Integer, ForeignKey('albums.ALBUM_ID'), nullable=False)
    GENRE_ID: Mapped[int] = mapped_column(Integer, ForeignKey('genres.GENRE_ID'), nullable=False)
    FILE_ID: Mapped[int] = mapped_column(Integer, ForeignKey('files.FILE_ID'), nullable=False)
    DURATION: Mapped[int] = mapped_column(Integer)
    FILE_PATH: Mapped[str] = mapped_column(String(255), nullable=False)
    BIT_RATE: Mapped[int] = mapped_column(Integer)
    SAMPLE_RATE: Mapped[int] = mapped_column(Integer)
    SONG_TITLE: Mapped[str] = mapped_column(String(100))
    RELEASE_DATE: Mapped[Date] = mapped_column(Date)

    FILE: Mapped['File'] = relationship("File", back_populates="SONGS")
    ALBUM: Mapped['Album'] = relationship("Album", back_populates="SONGS")
    GENRE: Mapped['Genre'] = relationship("Genre", back_populates="SONGS")