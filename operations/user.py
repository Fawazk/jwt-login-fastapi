from fastapi import HTTPException, HTTPException, status, Depends
import models.user as models
import models.contact as contact_models
import models.address as address_models
from schemas import user as UserSchema
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from database import get_db
import asyncio
from sqlmodel import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/login")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:80/login")


def verify_password(plain_password, password):
    return pwd_context.verify(plain_password, password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    user = db.query(models.User).where(models.User.username == username).all()
    if user:
        user_dict = vars(user[0])
        return UserSchema.FinalUserData(**user_dict)
    else:
        return {}


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = UserSchema.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: UserSchema.FinalUserData = Depends(get_current_user),
):
    if current_user:
        if current_user.is_active:
            return current_user
        else:
            raise HTTPException(status_code=400, detail="Inactive user")
    else:
        raise HTTPException(status_code=400, detail="User is None pls login")


def login_operation(db, form_data: UserSchema.LoginData):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def add_user(db, userdata: UserSchema.UserData):
    """This is the function for adding the users"""
    password = get_password_hash(userdata.password)
    userdata.password = password
    userdata = models.User(**userdata.dict())
    db.add(userdata)
    db.commit()
    db.refresh(userdata)
    return userdata


# def get_users(db,user_id=None,skip=0,limit=100):
def get_users(**kwargs):

    if "db" in kwargs:
        db = kwargs["db"]

        if "skip" in kwargs:
            skip = kwargs["skip"]

        if "limit" in kwargs:
            limit = kwargs["limit"]

        if "user_id" in kwargs:
            user_id = kwargs["user_id"]
            list_of_users = db.get(models.User, user_id)
        else:
            list_of_users = db.query(models.User).offset(skip).limit(limit).all()
        if list_of_users:
            return list_of_users
        else:
            raise HTTPException(
                status_code=502,
                detail="This user id is not found in our database . pls enter any correct usesr id",
            )
    else:
        raise HTTPException(status_code=502, detail="Database error")


def edit_user(db, userdata, user_id):
    print(user_id, "user_iduser_iduser_iduser_id")
    address = db.get(models.User, user_id)
    if address:
        address_data = userdata.dict(exclude_unset=True)
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


def delete_user(db, user):
    user_id = user.id
    related_dbs = {}
    related_dbs["contact"] = (
        db.query(contact_models.ContactInfo)
        .filter(contact_models.ContactInfo.user_id == user_id)
        .all()
    )
    related_dbs["address"] = (
        db.query(address_models.Addressess)
        .filter(address_models.Addressess.user_id == user_id)
        .all()
    )
    user_db = db.query(models.User).where(models.User.id == user_id).all()
    related_dbs["user"] = user_db
    if user_db:
        for related_db in related_dbs:
            for data in related_dbs[related_db]:
                db.delete(data)
                db.commit()
        return {"Is_deleted": True}
    else:
        raise HTTPException(
            status_code=404,
            detail="This user id is not found in our database . pls enter any correct user id",
        )
