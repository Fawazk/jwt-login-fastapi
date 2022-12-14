from pydantic import BaseModel
from typing import Optional


    
#  Address Schema
class AddressData(BaseModel):
    country : str  
    city : str 

class FinalAddressData(AddressData):
    id:int
    user_id:int

    class Config:
        orm_mode = True