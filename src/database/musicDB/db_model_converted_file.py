from sqlalchemy import Integer, Enum, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship, Mapped, mapped_column
from musicApp.src.database.musicDB.db import Base


class ConvertedFile(Base):
    __tablename__ = 'converted_files'

    CONVERSION_ID: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, index=True)
    ORIGINAL_FILE_ID: Mapped[int] = mapped_column(Integer, ForeignKey('files.FILE_ID'), nullable=False)
    FILE_DATA: Mapped[LargeBinary] = mapped_column(LargeBinary)
    FILE_TYPE: Mapped[str] = mapped_column(Enum('wav', 'rar'))

    ORIGINAL_FILE: Mapped['File'] = relationship("File", back_populates="CONVERTED_FILES")
