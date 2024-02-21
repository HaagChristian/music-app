from sqlalchemy import Column, Integer, String, Date, Enum, ForeignKey, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column
from musicApp.src.database.musicDB.db import Base


class File(Base):
    __tablename__ = 'files'

    FILE_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    FILE_DATA: Mapped[LargeBinary] = mapped_column(LargeBinary)
    FILE_TYPE: Mapped[str] = mapped_column(Enum('mp3', 'wav', 'rar'))
