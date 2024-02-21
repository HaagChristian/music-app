from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from musicApp.src.database.userDB.db import Base


class Address(Base):
    __tablename__ = "address"

    ADDRESS_ID: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    STREET: Mapped[str] = mapped_column(nullable=False)
    HOUSE_NUMBER: Mapped[int] = mapped_column(nullable=False)
    POSTAL_CODE: Mapped[int] = mapped_column(nullable=False)
    CITY: Mapped[str] = mapped_column(nullable=False)
    COUNTRY: Mapped[str] = mapped_column(nullable=False)
    STATE: Mapped[str] = mapped_column(nullable=False)
    USER_ID: Mapped[int] = mapped_column(ForeignKey('user.ID'), nullable=False)

    user: Mapped["User"] = relationship(back_populates="address", lazy=True)  # specify lazy loading
