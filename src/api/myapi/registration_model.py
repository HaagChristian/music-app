from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator, Field


class Address(BaseModel):
    street: str = Field(..., min_length=3, max_length=256)
    house_number: int
    postal_code: int
    city: str = Field(..., min_length=3, max_length=256)
    country: str = Field(..., min_length=3, max_length=256)
    state: Optional[str] = Field(None, min_length=3, max_length=256)


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class AuthUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True


# Input models

class SignInRequestModel(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=3, max_length=256)


class SignUpRequestModel(BaseModel):
    email: EmailStr = Field(..., max_length=256)
    password: str = Field(..., max_length=256)
    first_name: str = Field(..., min_length=3, max_length=256)
    last_name: str = Field(..., min_length=3, max_length=256)
    username: str = Field(..., min_length=3, max_length=256)
    address: Address = Field(..., min_length=3, max_length=256)

    @field_validator("password")
    def password_validator(cls, v):
        # If length of password is less than 8, raise a validation error
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


# Output models

class SignUpUserResponse(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str


class UserAuthResponseModel(BaseModel):
    token: TokenModel
