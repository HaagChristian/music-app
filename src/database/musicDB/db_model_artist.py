from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.musicDB.db import Base


class Artist(Base):
    __tablename__ = 'artists'

    ARTIST_ID: Mapped[int] = mapped_column(Integer, primary_key=True)
    ARTIST_NAME: Mapped[str] = mapped_column(String(100))

    album: Mapped['Album'] = relationship(back_populates="artist")
