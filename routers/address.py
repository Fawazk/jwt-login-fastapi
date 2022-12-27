from fastapi import FastAPI, HTTPException, Depends, APIRouter, Response
import models.contact as ContactModels
import models.user as UserModels
from database import engine, get_db
from sqlmodel import Session, SQLModel, select
from operations import address as functions, user as user_functions
from schemas import address as AddressSchema, user as UserSchema


router = APIRouter(
    tags=["Address"],
)


# Address
@router.post("/add_address", response_model=AddressSchema.FinalAddressData)
async def Add_address(
    addressdata: AddressSchema.AddressData,
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To add the address to user id"""
    user_id = current_user.id
    user = db.get(UserModels.User, user_id)
    if user:
        response = functions.add_address(db, addressdata, user_id)
        return response
    else:
        raise HTTPException(
            status_code=404,
            detail="This user id is not found in our database. pls enter any correct user id",
        )


@router.get("/get_address/{user_id}")
async def get_address(
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To get the address filltered by user id"""
    user_id = current_user.id
    response = functions.get_address(db, user_id)
    return response


@router.patch(
    "/edit_address/{address_id}", response_model=AddressSchema.FinalAddressData
)
async def edit_address(
    addressdata: AddressSchema.AddressData,
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To edit the address"""
    response = functions.edit_address(db, addressdata, address_id)
    return response


@router.delete("/delete_address/{address_id}")
async def delete_address(
    address_id: int,
    db: Session = Depends(get_db),
    current_user: UserSchema.FinalUserData = Depends(
        user_functions.get_current_active_user
    ),
):
    """To delete the address"""
    response = functions.delete_address(db, address_id)
    return response
