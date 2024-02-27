from io import BytesIO

import pytest
from fastapi import UploadFile
from starlette.testclient import TestClient

from main import app
from src.api.middleware.auth import AuthProvider
from src.api.middleware.authjwt import AuthJwt


@pytest.fixture(scope='session')
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def create_upload_file():
    def _create_upload_file(content: bytes, filename: str):
        return UploadFile(filename=filename, file=BytesIO(content))

    return _create_upload_file


@pytest.fixture
def auth_jwt():
    return AuthJwt()


@pytest.fixture
def auth_provider():
    return AuthProvider()
