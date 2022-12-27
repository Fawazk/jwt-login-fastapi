from sqlmodel import Field, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: Optional[str] = Field(default=None, unique=True)
    full_name: str
    password: str
    is_active: Optional[bool] = Field(default=True)
    is_super_user: Optional[bool] = Field(default=False)
