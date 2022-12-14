

from sqlmodel import Field, SQLModel
from typing import Optional



class Addressess(SQLModel,table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id : Optional[int] = Field(foreign_key="user.id")
    # user_id: Optional[int] = Field(sa_column=Column(Integer, ForeignKey("user.id", ondelete="CASCADE")))
    country : str   
    city : str
