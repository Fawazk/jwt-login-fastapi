from fastapi import HTTPException
import models.address as models
import models.user as user_model
from schemas import address as AddressSchema


#  Address functions
def add_address(db, addressdata: AddressSchema.AddressData, user_id):
    addressdata_db = models.Addressess(**addressdata.dict(), user_id=user_id)
    db.add(addressdata_db)
    db.commit()
    db.refresh(addressdata_db)
    return addressdata_db


def get_address(db, user_id):
    user = db.get(user_model.User, user_id)
    if user:
        list_of_address = (
            db.query(models.Addressess)
            .filter(models.Addressess.user_id == user_id)
            .all()
        )
        if list_of_address:
            return list_of_address
        else:
            return [
                {
                    "detail": "This user have no address data in our database , pls add address"
                }
            ]
    else:
        raise HTTPException(
            status_code=404,
            detail="This user id is not found in our database . pls enter any correct user id",
        )


def edit_address(db, addressdata, address_id):
    address = db.get(models.Addressess, address_id)
    if address:
        address_data = addressdata.dict(exclude_unset=True)
        for key, value in address_data.items():
            setattr(address, key, value)
        db.add(address)
        db.commit()
        db.refresh(address)
        return address
    else:
        raise HTTPException(
            status_code=404,
            detail="This address id is not found in our database . pls enter any correct address id",
        )


def delete_address(db, address_id):
    address = db.get(models.Addressess, address_id)
    if address:
        db.delete(address)
        db.commit()
        return {"Is_deleted": True}
    else:
        raise HTTPException(
            status_code=404,
            detail="This address id is not found in our database . pls enter any correct address id",
        )
