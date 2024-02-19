from unittest.mock import patch

from sqlalchemy.exc import NoResultFound
from starlette import status
from starlette.testclient import TestClient

from src.api.myapi.registration_model import SignInRequestModel
from src.database.db_model_address import Address
from src.database.db_model_user import User
from src.service.registration.signup_user import auth_handler

# mock test data
signin_instance = SignInRequestModel(email="example@example.com", password="password123")

address_data = Address(STREET="123 Main St", HOUSE_NUMBER=10, POSTAL_CODE=12345, CITY="Test City",
                       COUNTRY="Test Country", STATE="Test State")

user_data = User(ID=1, USERNAME="test_user", FIRST_NAME="Test", LAST_NAME="User", EMAIL=signin_instance.email,
                 PASSWORD_HASH="hashed_password", address=[address_data])


# Mock the database query to return the user data
def mock_get_user_by_email(email: str):
    if email == "test@example.com":
        return user_data
    else:
        raise NoResultFound("User not found")


@patch.object(auth_handler, "authenticate_user", return_value=user_data)
@patch.object(User, "get_user_by_email", side_effect=mock_get_user_by_email)
def test_signin_endpoint(mock_authenticate_user, mock_get_user_by_email, client: TestClient):
    # Patch the authenticate_user function to return the user data

    response = client.post("/api/registration/auth/signin", json=signin_instance.dict())

    # Check if the response status code is 200
    assert response.status_code == status.HTTP_200_OK

    # Check if the response contains the expected data
    response_data = response.json()
    assert "token" in response_data
    assert "access_token" in response_data["token"]
    assert "refresh_token" in response_data["token"]
    assert response_data["token"]["access_token"] != ""
    assert response_data["token"]["refresh_token"] != ""
