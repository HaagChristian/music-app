from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from src.api.myapi.registration_model import Address


class UserUpdateRequestModel(BaseModel):
    id: int
    email: EmailStr
    password: Optional[str] = None
    first_name: str
    last_name: str

    @field_validator("password")
    def password_validator(cls, v):
        # If the password is an empty string or None, set it to None
        if v == "" or v is None:
            return None
        # If length of password is less than 8, raise a validation error
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class UserResponseModel(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    username: str
    address: Address
