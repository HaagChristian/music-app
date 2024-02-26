from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.api.myapi.registration_model import Address
from src.api.myapi.user_model import UserResponseModel
from src.database.userDB.db_model_user import User
from src.settings.error_messages import DB_NO_RESULT_FOUND


def get_current_user(jwt_payload: str, db: Session):
    user_data = User.get_user_by_email(db=db, email=jwt_payload)

    if not user_data:
        # wrong credentials because no user is found with the given email
        raise NoResultFound(DB_NO_RESULT_FOUND)

    # Map db model to output model
    return UserResponseModel(
        id=user_data.ID,
        email=user_data.EMAIL,
        first_name=user_data.FIRST_NAME,
        last_name=user_data.LAST_NAME,
        username=user_data.USERNAME,
        address=Address(
            street=user_data.address[0].STREET,
            house_number=user_data.address[0].HOUSE_NUMBER,
            postal_code=user_data.address[0].POSTAL_CODE,
            city=user_data.address[0].CITY,
            country=user_data.address[0].COUNTRY,
            state=user_data.address[0].STATE)
    )
