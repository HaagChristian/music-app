from typing import List, Type

from sqlalchemy.orm import Session, relationship, Mapped, mapped_column

from src.api.myapi.registration_model import SignUpRequestModel
from src.database.db import Base
from src.database.db_model_address import Address


class User(Base):
    __tablename__ = "user"

    ID: Mapped[int] = mapped_column(primary_key=True, nullable=False, index=True)
    USERNAME: Mapped[str] = mapped_column(nullable=False)
    FIRST_NAME: Mapped[str] = mapped_column(nullable=False)
    LAST_NAME: Mapped[str] = mapped_column(nullable=False)
    EMAIL: Mapped[str] = mapped_column(nullable=False)
    PASSWORD_HASH: Mapped[str] = mapped_column(nullable=False)

    address: Mapped[List["Address"]] = relationship(back_populates="user", lazy=True)

    # address is specified as list, because a user can have multiple addresses

    # specify lazy loading
    # --> load relationship with additional query when the attribute is first accessed

    @staticmethod
    def write_data_to_db(db: Session, user_data: SignUpRequestModel, encrypted_password: str):
        new_address = Address(
            STREET=user_data.address.street,
            HOUSE_NUMBER=user_data.address.house_number,
            POSTAL_CODE=user_data.address.postal_code,
            CITY=user_data.address.city,
            COUNTRY=user_data.address.country,
            STATE=user_data.address.state
        )

        new_user = User(
            FIRST_NAME=user_data.first_name,
            LAST_NAME=user_data.last_name,
            EMAIL=user_data.email,
            PASSWORD_HASH=encrypted_password,
            USERNAME=user_data.username,
            address=[new_address])

        db.add(new_user)
        db.flush()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Type['User']:
        query = db.query(User).filter(User.EMAIL == email)
        return query.first()
