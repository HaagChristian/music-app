from pydantic import BaseModel, EmailStr

from src.api.myapi.registration_model import Address


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    address: Address
