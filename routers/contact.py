from fastapi import FastAPI, HTTPException, Depends, APIRouter
import models.contact as ContactModels
from database import engine, get_db
from sqlmodel import Session, SQLModel, select
from operations import contact as functions
from operations import user as user_functions
from schemas import contact as ContactSchema, user as UserSchema

# import ipdb
from sqlalchemy import exc

router = APIRouter(
    tags=["Contact"],
)


# contact info


@router.post("/add_contact", response_model=ContactSchema.FinalContactInfoData)
async def Add_contact(
    contactdata: ContactSchema.ContactInfoData,
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To add the contact to user id"""
    user_id = current_user.id
    try:
        response = functions.add_contact(db, contactdata, user_id)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e.orig))
    return response


@router.get("/get_contact/{user_id}")
async def get_contact(
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To get the all the contact of a user"""
    user_id = current_user.id
    response = functions.get_contact(db, user_id)
    return response


@router.patch(
    "/edit_contact/{contact_id}", response_model=ContactSchema.FinalContactInfoData
)
# async def edit_contact(contactdata: ContactSchema.ContactInfoData,contact_id:int,db:Session = Depends(get_db)):
async def edit_address(
    contactdata: ContactSchema.ContactInfoData,
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To edit the user contact based on te given id"""
    try:
        response = functions.edit_contact(db, contactdata, contact_id)
    except exc.IntegrityError as e:
        raise HTTPException(status_code=409, detail=str(e.orig))
    return response


@router.delete("/delete_contact/{contact_id}")
async def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    response = functions.delete_contact(db, contact_id)
    return response
