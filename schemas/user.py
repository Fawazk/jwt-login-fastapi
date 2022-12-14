
from pydantic import BaseModel, validator
from typing import Optional


# pertner Schema
class Token(BaseModel):
    access_token: str
    token_type: str


# class TokenData(BaseModel):
#     username: str | None = None
class TokenData(BaseModel):
    username: str | None = None

class LoginData(TokenData):
    password: str


class UserData(LoginData):
    full_name: str


class FinalSuperUserData(UserData):
    id: int
    is_super_user: bool

    class Config:
        validate_assignment = True

    @validator('is_super_user')
    def set_is_super_user(cls, is_super_user):
        return True


class FinalUserData(UserData):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class UserAllData(BaseModel):
    user: Optional[FinalUserData]
    address: list
    contact: list
