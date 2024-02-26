from datetime import datetime, timedelta

import jwt
from fastapi.security import HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, DecodeError
from sqlalchemy.exc import NoResultFound

from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.settings.error_messages import DB_NO_RESULT_FOUND, JWT_INVALID_TOKEN
from src.settings.settings import TIMEZONE, TOKEN_EXPIRE_MINS, SECRET_KEY, ALGORITHM, REFRESH_TOKEN_EXPIRE_HOURS


class AuthJwt:
    """ Authentication class to:
        - decode token
        - encode token
        - create refresh token
    """

    def __init__(self):
        self._decoded_jwt: dict = {}

    def decode_token(self, jwt_token: HTTPAuthorizationCredentials):
        if not jwt_token.scheme == "Bearer" or not self.decode_jwt(jwt_token.credentials):
            raise Unauthorized(JWT_INVALID_TOKEN)
        return self._decoded_jwt

    def decode_jwt(self, token: str) -> dict | None:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
            if datetime.fromtimestamp(decoded_token['exp']) >= datetime.now():
                self._decoded_jwt = decoded_token
                return self._decoded_jwt
        except (ExpiredSignatureError, DecodeError):  # Decode Error occurs when Bearer is invalid
            return None

    def refresh_token(self, refresh_token: HTTPAuthorizationCredentials) -> str:
        try:
            self.decode_token(refresh_token)
            if self._decoded_jwt["scope"] == "refresh_token":
                user_email = self._decoded_jwt["sub"]
                new_token = self.encode_token(user_email)
                return new_token
        except(jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            raise NoResultFound(DB_NO_RESULT_FOUND)

    @property
    def get_token_data_from_decoded_token(self) -> str:
        return self._decoded_jwt['sub']

    @staticmethod
    def encode_token(user_email) -> str:
        payload = {
            "exp": datetime.now(TIMEZONE) + timedelta(days=0, minutes=TOKEN_EXPIRE_MINS),
            "iat": datetime.now(TIMEZONE),
            "scope": "access_token",
            "sub": user_email,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def encode_refresh_token(user_email) -> str:
        payload = {
            "exp": datetime.now(TIMEZONE) + timedelta(days=0, hours=REFRESH_TOKEN_EXPIRE_HOURS),
            "iat": datetime.now(TIMEZONE),
            "scope": "refresh_token",
            "sub": user_email,
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
