from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database.musicDB.db import Base


class Album(Base):
    __tablename__ = 'albums'

    ALBUM_ID: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    ALBUM_NAME: Mapped[str] = mapped_column(String(100))
    ARTIST_ID: Mapped[int] = mapped_column(ForeignKey('artists.ARTIST_ID'), nullable=False)

    artist: Mapped['Artist'] = relationship(back_populates="album")
    song: Mapped['Song'] = relationship(back_populates="album")
