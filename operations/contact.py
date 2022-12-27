from fastapi import HTTPException
import models.user as UserModels
import models.address as AddressModels
import models.contact as ContactModels
from schemas import contact as ContactSchema


# contact functions
def add_contact(db, contactdata: ContactSchema.ContactInfoData, user_id):
    """Tis is the function for adding the contactinfo with a user"""
    user = db.get(UserModels.User, user_id)
    if user:
        contactdata_db = ContactModels.ContactInfo(
            **contactdata.dict(), user_id=user_id
        )
        db.flush()

        db.add(contactdata_db)
        db.commit()
        db.refresh(contactdata_db)
        return contactdata_db
    else:
        raise HTTPException(
            status_code=404,
            detail="This user id is not found in our database . pls enter any correct user id",
        )


def get_contact(db, user_id):
    user = db.get(UserModels.User, user_id)
    if user:
        list_of_contact = (
            db.query(ContactModels.ContactInfo)
            .filter(ContactModels.ContactInfo.user_id == user_id)
            .all()
        )
        if list_of_contact:
            return list_of_contact
        else:
            return [
                {
                    "detail": "This user have no contact data in our database , pls add contact"
                }
            ]
    else:
        raise HTTPException(
            status_code=404,
            detail="This user id is not found in our database . pls enter any correct user id",
        )


def edit_contact(db, contactdata, contact_id):
    contact = db.get(ContactModels.ContactInfo, contact_id)
    if contact:
        contact_data = contactdata.dict(exclude_unset=True)
        for key, value in contact_data.items():
            setattr(contact, key, value)
        db.add(contact)
        db.commit()
        db.refresh(contact)
        return contact
    else:
        raise HTTPException(
            status_code=404,
            detail="This contact id is not found in our database . pls enter any correct contact id",
        )


def delete_contact(db, contact_id):
    contact = db.get(ContactModels.ContactInfo, contact_id)
    if contact:
        db.delete(contact)
        db.commit()
        return {"Is_deleted": True}
    else:
        raise HTTPException(
            status_code=404,
            detail="This contact id is not found in our database . pls enter any correct contact id",
        )
