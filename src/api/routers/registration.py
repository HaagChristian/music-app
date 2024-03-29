from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.requests import Request

from src.api.middleware.auth import AuthProvider
from src.api.middleware.authjwt import AuthJwt
from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.api.middleware.custom_exceptions.user_already_exist import UserAlreadyExistException
from src.api.middleware.exceptions import exception_mapping
from src.api.myapi.registration_model import UserAuthResponseModel, SignUpRequestModel, SignInRequestModel, \
    SignUpUserResponse, \
    TokenModel, AuthUser
from src.database.user_db.db import get_db_user, commit_on_signup
from src.service.registration.signup_user import register_user, signin_user
from src.settings.error_messages import INVALID_REFRESH_TOKEN

router = APIRouter(
    prefix="/api/registration", tags=["Create a User"]
)

auth_handler = AuthProvider()
http_bearer = HTTPBearer()


@router.post("/auth/signup", response_model=SignUpUserResponse)
@commit_on_signup
def signup(request: Request, user: SignUpRequestModel, response: Response, db=Depends(get_db_user)):
    """
        API call to register a new user/account

        \f
        :param request: Request is used for the decorator commit_on_signup
        :param user: SignUpRequestModel contains the user details
        :param response: Response is used for the decorator commit_on_signup
        :param db: Database connection
    """
    try:
        output_user: SignUpUserResponse = register_user(user_model=user, db=db)
        response.status_code = status.HTTP_201_CREATED
        return output_user
    except (UserAlreadyExistException, NoResultFound) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))


@router.post("/auth/signin", response_model=UserAuthResponseModel)
def signin_api(user_details: SignInRequestModel, db=Depends(get_db_user)):
    """ API call to sign in a user/account and return a token and refresh token """
    try:
        user: AuthUser = signin_user(email=user_details.email, password=user_details.password, db=db)
        access_token = AuthJwt.encode_token(user.email)
        refresh_token = AuthJwt.encode_refresh_token(user.email)

        return UserAuthResponseModel(token=TokenModel(access_token=access_token, refresh_token=refresh_token))
    except NoResultFound as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))


@router.post("/auth/refresh", response_model=UserAuthResponseModel)
def new_token_from_refresh_token(token: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)]):
    """ API call to refresh a token and return a new token and refresh token """
    try:
        auth = AuthJwt()
        access_token = auth.refresh_token(refresh_token=token)
        if not access_token:
            raise Unauthorized(INVALID_REFRESH_TOKEN)
        refresh_token = AuthJwt.encode_refresh_token(user_email=auth.get_token_data_from_decoded_token)

        return UserAuthResponseModel(token=TokenModel(access_token=access_token, refresh_token=refresh_token))
    except (NoResultFound, Unauthorized) as e:
        http_status, detail_function = exception_mapping.get(type(e), (
            status.HTTP_500_INTERNAL_SERVER_ERROR, lambda e: str(e.args[0])))
        raise HTTPException(status_code=http_status, detail=detail_function(e))
