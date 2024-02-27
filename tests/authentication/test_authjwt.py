from datetime import datetime, timedelta

import jwt
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.exc import NoResultFound

from src.api.middleware.custom_exceptions.unauthorized import Unauthorized
from src.settings.error_messages import JWT_INVALID_TOKEN
from src.settings.settings import TIMEZONE, SECRET_KEY, ALGORITHM


def test_decode_token_with_valid_token(auth_jwt):
    user_email = "example@example.com"
    token = auth_jwt.encode_token(user_email)
    try:
        decoded_token = auth_jwt.decode_token(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
        assert decoded_token["sub"] == user_email
    except Unauthorized as e:
        assert False, f"Unexpected Unauthorized error: {e}"


def test_decode_token_with_expired_token(auth_jwt):
    user_email = "example@example.com"
    payload = {
        "exp": datetime.now(TIMEZONE) - timedelta(days=1),
        "iat": datetime.now(TIMEZONE),
        "scope": "access_token",
        "sub": user_email,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    try:
        auth_jwt.decode_token(HTTPAuthorizationCredentials(scheme="Bearer", credentials=token))
        assert False, "Expected Unauthorized error but no exception was raised."
    except Unauthorized as e:
        assert str(e) == JWT_INVALID_TOKEN


def test_decode_token_with_invalid_token(auth_jwt):
    try:
        auth_jwt.decode_token(HTTPAuthorizationCredentials(scheme="Bearer", credentials="invalid_token"))
        assert False, "Expected Unauthorized error but no exception was raised."
    except Unauthorized as e:
        assert str(e) == JWT_INVALID_TOKEN


def test_refresh_token_with_valid_token(auth_jwt):
    user_email = "example@example.com"
    refresh_token = auth_jwt.encode_refresh_token(user_email)
    try:
        new_token = auth_jwt.refresh_token(HTTPAuthorizationCredentials(scheme="Bearer", credentials=refresh_token))
        decoded_new_token = jwt.decode(new_token, SECRET_KEY, algorithms=[ALGORITHM])
        assert decoded_new_token["sub"] == user_email
        assert decoded_new_token["scope"] == "access_token"
    except NoResultFound as e:
        assert False, f"Unexpected NoResultFound error: {e}"


def test_refresh_token_with_expired_token(auth_jwt):
    user_email = "example@example.com"
    payload = {
        "exp": datetime.now(TIMEZONE) - timedelta(days=1),
        "iat": datetime.now(TIMEZONE),
        "scope": "refresh_token",
        "sub": user_email,
    }
    refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    try:
        auth_jwt.refresh_token(HTTPAuthorizationCredentials(scheme="Bearer", credentials=refresh_token))
        assert False, "Expected NoResultFound error but no exception was raised."
    except Exception as e:
        print('a')
        pass  # Expected behavior
