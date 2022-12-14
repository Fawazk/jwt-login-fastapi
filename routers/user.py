from fastapi import (FastAPI, Depends, APIRouter)
from operations import user as functions, address as Address_functions, contact as Contact_functions
from database import get_db
from sqlmodel import Session
from schemas import user as UserSchema
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(tags=["user"])

# user
@router.post("/register", response_model=UserSchema.FinalUserData)
async def Add_user(Userdata: UserSchema.UserData, db: Session = Depends(get_db)):
    """To add the user """
    response = functions.add_user(db, Userdata)
    return response


@router.post("/register-super-user", response_model=UserSchema.FinalSuperUserData)
async def Add_super_user(Userdata: UserSchema.UserData, db: Session = Depends(get_db)):
    """To add the user """
    response = functions.add_user(db, Userdata)
    return response


 

@router.post("/login", response_model=UserSchema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    response = functions.login_operation(db,form_data)
    return response



@router.get("/get_users", response_model=list[UserSchema.FinalUserData])
async def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),current_user: UserSchema.FinalUserData = Depends(functions.get_current_active_user)):
    """To get the all users (address and contact is not included)"""
    response = functions.get_users(db=db, skip=skip, limit=limit)
    return response


@router.get("/get_user", response_model=UserSchema.FinalUserData)
async def get_users(user_id: int, db: Session = Depends(get_db),current_user: UserSchema.FinalUserData = Depends(functions.get_current_active_user)):
    """To get one user by the id given"""
    response = functions.get_users(db=db, user_id=user_id)
    return response


@router.patch("/edit_user", response_model=UserSchema.FinalUserData)
async def edit_user(Userdata: UserSchema.UserData, user_id: int, db: Session = Depends(get_db),current_user: UserSchema.FinalUserData = Depends(functions.get_current_active_user)):
    """To edit the user data (Username,password) which filtered by given id"""
    response = functions.edit_user(db, Userdata, user_id)
    return response


@router.delete("/delete_users")
async def delete_user(user_id: int, db: Session = Depends(get_db),current_user: UserSchema.FinalUserData = Depends(functions.get_current_active_user)):
    """To delete the entire user and realated datas (address and contact)"""
    response = functions.delete_user(db, user_id)
    return response


# @router.get("/user-all-data",response_model=userSchema.userAllData, tags=["user with all datas"])
@router.get("/user-all-data")
async def user_all_data(user_id: int, db: Session = Depends(get_db),current_user: UserSchema.FinalUserData = Depends(functions.get_current_active_user)):
    """This Api will show all the data's related to the user id which you passed"""
    userresponse = functions.get_users(db=db, user_id=user_id)
    addressresponse = Address_functions.get_address(db, user_id)
    contactresponse = Contact_functions.get_contact(db, user_id)
    response = {}
    response["user"] = userresponse
    response['address'] = addressresponse
    response['contact'] = contactresponse
    return response
