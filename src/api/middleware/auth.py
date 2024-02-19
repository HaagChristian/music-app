from typing import Type

from passlib.context import CryptContext
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.api.myapi.registration_model import AuthUser
from src.database.db_model_user import User
from src.settings.error_messages import DB_NO_RESULT_FOUND


class AuthProvider:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.PWD_CONTEXT.verify(plain_password, hashed_password)

    def get_password_hash(self, password) -> str:
        return self.PWD_CONTEXT.hash(password)

    def authenticate_user(self, user_email: str, password: str, db: Session) -> AuthUser:
        user_from_db: Type['User'] = User.get_user_by_email(db=db, email=user_email)

        if not user_from_db or not self.verify_password(password, user_from_db.PASSWORD_HASH):
            # password is wrong --> due to security throw same error
            raise NoResultFound(DB_NO_RESULT_FOUND)

        return AuthUser(id=user_from_db.ID, first_name=user_from_db.FIRST_NAME, last_name=user_from_db.LAST_NAME,
                        email=user_from_db.EMAIL)
