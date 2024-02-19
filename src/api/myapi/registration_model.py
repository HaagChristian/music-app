from pydantic import BaseModel, EmailStr, field_validator


class SignInRequestModel(BaseModel):
    email: str
    password: str


class Address(BaseModel):
    street: str
    house_number: int
    postal_code: int
    city: str
    country: str
    state: str


class SignUpRequestModel(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    username: str
    address: Address

    @field_validator("password")
    def password_validator(cls, v):
        # If length of password is less than 8, raise a validation error
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v


class SignUpUser(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    username: str


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str


class UserAuthResponseModel(BaseModel):
    token: TokenModel


class AuthUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str

    class Config:
        from_attributes = True
