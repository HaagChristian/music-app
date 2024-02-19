from starlette.testclient import TestClient

from main import app
from src.api.myapi.registration_model import SignUpRequestModel, Address, SignUpUser
from src.database.db import get_db
from tests.conftest import mock_db

app.dependency_overrides[get_db] = mock_db()

# Request data
signup_instance = SignUpRequestModel(
    email="example@example.com",
    password="password123",
    first_name="John",
    last_name="Doe",
    username="johndoe",
    address=Address(
        street="123 Main St",
        house_number=10,
        postal_code=12345,
        city="Example City",
        country="Example Country",
        state="Example State"
    )
)

# Response data
response_signup = SignUpUser(
    email="example@example.com",
    first_name="John",
    last_name="Doe",
    username="johndoe")


def test_signup(client: TestClient):
    response = client.post('/api/registration/auth/signup', json=signup_instance.dict())
    assert response.status_code == 201

    assert response.json() == response_signup.dict()


def test_signup_invalid_email(client: TestClient):
    signup_instance.email = "example.com"
    response = client.post('/api/registration/auth/signup', json=signup_instance.dict())
    assert response.status_code == 422
    assert response.json() == {'detail': [{'ctx': {'reason': 'The email address is not valid. It must have '
                                                             'exactly one @-sign.'},
                                           'input': 'example.com',
                                           'loc': ['body', 'email'],
                                           'msg': 'value is not a valid email address: The email address is '
                                                  'not valid. It must have exactly one @-sign.',
                                           'type': 'value_error'}]}
