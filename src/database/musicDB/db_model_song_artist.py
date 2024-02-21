from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database.musicDB.db import Base


class SongArtist(Base):
    __tablename__ = 'songs_artists'

    SONG_ID: Mapped[int] = mapped_column(Integer, ForeignKey('songs.SONG_ID'), primary_key=True, nullable=False,
                                         index=True)
    ARTIST_ID: Mapped[int] = mapped_column(Integer, ForeignKey('artists.ARTIST_ID'), primary_key=True, nullable=False,
                                           index=True)

    song: Mapped['Song'] = relationship(back_populates="songs_artist")
    artist: Mapped['Artist'] = relationship(back_populates="songs_artist")
