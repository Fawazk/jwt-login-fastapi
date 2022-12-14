

from sqlmodel import Field, SQLModel
from typing import Optional




class ContactInfo(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : Optional[int] = Field(foreign_key="user.id")
    # user_id : Optional[int] = Field(sa_column=Column(Integer, ForeignKey("user.id", ondelete="CASCADE")))
    mobile_phone : Optional[str] = Field(default=None,unique=True)
    email : Optional[str] = Field(default=None,unique=True)