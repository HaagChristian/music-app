from unittest.mock import Mock

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.settings.error_messages import DB_NO_RESULT_FOUND

user_mock = Mock(ID=1, FIRST_NAME='John', LAST_NAME='Doe', EMAIL='john.doe@example.com',
                 PASSWORD_HASH='',
                 PLAIN_PASSWORD='password123')


def test_get_password_hash(auth_provider):
    password = user_mock.PLAIN_PASSWORD
    hashed_password = auth_provider.get_password_hash(password)
    user_mock.PASSWORD_HASH = hashed_password
    assert len(hashed_password) > 0
    assert hashed_password != password


def test_verify_password_with_valid_password(auth_provider):
    hashed_password = user_mock.PASSWORD_HASH
    plain_password = user_mock.PLAIN_PASSWORD
    assert auth_provider.verify_password(plain_password, hashed_password) is True


def test_verify_password_with_invalid_password(auth_provider):
    hashed_password = user_mock.PASSWORD_HASH
    plain_password = "wrong_password"
    assert not auth_provider.verify_password(plain_password, hashed_password)


def test_authenticate_user_with_valid_credentials(auth_provider, monkeypatch):
    user_mock_valid = Mock()
    user_mock_valid.ID = 123
    user_mock_valid.FIRST_NAME = "John"
    user_mock_valid.LAST_NAME = "Doe"
    user_mock_valid.EMAIL = "john.doe@example.com"
    user_mock_valid.PASSWORD_HASH = user_mock.PASSWORD_HASH

    def mock_get_user_by_email(db: Session, email: str):
        return user_mock_valid

    monkeypatch.setattr('src.database.user_db.db_model_user.User.get_user_by_email', mock_get_user_by_email)
    user_email = "john.doe@example.com"
    password = "password123"
    db = Mock(Session)
    authenticated_user = auth_provider.authenticate_user(user_email, password, db)

    assert authenticated_user.id == user_mock_valid.ID
    assert authenticated_user.first_name == user_mock_valid.FIRST_NAME
    assert authenticated_user.last_name == user_mock_valid.LAST_NAME
    assert authenticated_user.email == user_mock_valid.EMAIL


def test_authenticate_user_with_invalid_credentials(auth_provider, monkeypatch):
    def mock_get_user_by_email(db: Session, email: str):
        return None

    monkeypatch.setattr('src.database.user_db.db_model_user.User.get_user_by_email', mock_get_user_by_email)
    user_email = "john.doe@example.com"
    password = "wrong_password"
    db = Mock(Session)
    try:
        auth_provider.authenticate_user(user_email, password, db)
        assert False, "Expected NoResultFound error but no exception was raised."
    except NoResultFound as e:
        assert type(e) is NoResultFound
        assert e.args[0] == DB_NO_RESULT_FOUND
