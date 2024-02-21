from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from musicApp.src.database.musicDB.db import Base


class SongArtist(Base):
    __tablename__ = 'songs_artists'

    SONG_ID: Mapped[int] = mapped_column(Integer, ForeignKey('songs.SONG_ID'), primary_key=True, nullable=False, index=True)
    ARTIST_ID: Mapped[int] = mapped_column(Integer, ForeignKey('artists.ARTIST_ID'), primary_key=True, nullable=False, index=True)

    SONG: Mapped['Song'] = relationship("Song", back_populates="SONG_ARTISTS")
    ARTIST: Mapped['Artist'] = relationship("Artist", back_populates="SONG_ARTISTS")
