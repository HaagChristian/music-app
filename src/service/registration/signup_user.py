from sqlalchemy.orm import Session

from src.api.middleware.auth import AuthProvider
from src.api.middleware.custom_exceptions.user_already_exist import UserAlreadyExistException
from src.api.myapi.registration_model import SignUpRequestModel, SignUpUser
from src.database.db_model_user import User
from src.settings.error_messages import DB_INTEGRITY_ERROR

auth_handler = AuthProvider()


def register_user(user_model: SignUpRequestModel, db: Session):
    user = User.get_user_by_email(db=db, email=user_model.email)

    if user:
        raise UserAlreadyExistException(DB_INTEGRITY_ERROR)  # E-mail (user)  already exists

    hashed_password = auth_handler.get_password_hash(user_model.password)
    User.write_data_to_db(db=db, user_data=user_model, encrypted_password=hashed_password)
    return SignUpUser(first_name=user_model.first_name, last_name=user_model.last_name, email=user_model.email,
                      username=user_model.username)  # Do not return the password hash or any sensitive information


def signin_user(email, password, db: Session):
    user = auth_handler.authenticate_user(user_email=email, password=password, db=db)
    return user
