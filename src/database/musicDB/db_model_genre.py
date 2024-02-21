from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from musicApp.src.database.musicDB.db import Base


class Genre(Base):
    __tablename__ = 'genres'

    GENRE_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    GENRE_NAME: Mapped[str] = mapped_column(String(100))

