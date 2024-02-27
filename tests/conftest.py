from io import BytesIO

import pytest
from fastapi import UploadFile
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from main import app
from src.api.middleware.authjwt import AuthJwt
from src.database.musicDB.db import Base


@pytest.fixture(scope='session')
def client() -> TestClient:
    return TestClient(app)


def mock_db():
    SQLALCHEMY_DATABASE_URL = "sqlite://"

    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def get_test_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    return get_test_db


@pytest.fixture
def create_upload_file():
    def _create_upload_file(content: bytes, filename: str):
        return UploadFile(filename=filename, file=BytesIO(content))

    return _create_upload_file


@pytest.fixture
def auth_jwt():
    return AuthJwt()
