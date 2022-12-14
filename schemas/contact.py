from pydantic import BaseModel,EmailStr
from typing import Optional
from typing import List
from .phonenumber import PhoneNumber




# Contact Schema
class ContactInfoData(BaseModel):
    email : EmailStr
    mobile_phone : PhoneNumber

    class Config:
        schema_extra = {
            "example": {
                "email":"example@example.com",
                "mobile_phone": "+123456789",
            }
        }


class FinalContactInfoData(ContactInfoData):
    id : int
    user_id : int

    class Config:
        orm_mode = True