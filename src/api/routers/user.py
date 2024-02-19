from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.exc import NoResultFound
from starlette import status

from src.api.middleware.authjwt import AuthJwt
from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.user_model import UserResponseModel
from src.database.db import get_db
from src.service.login.user_data import get_current_user

router = APIRouter(
    prefix="/api/user", tags=["Get User Data"]
)

http_bearer = HTTPBearer()


@router.get("/me", response_model=UserResponseModel)
def read_users_me(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)], db=Depends(get_db)):
    try:
        auth = AuthJwt()
        auth.decode_token(jwt_token=token)
        email_from_jwt = auth.get_token_data_from_decoded_token

        return get_current_user(jwt_payload=email_from_jwt, db=db)
    except (Unauthorized, NoResultFound) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
