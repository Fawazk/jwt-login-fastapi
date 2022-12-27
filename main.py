from fastapi import FastAPI, Request, status
from sqlmodel import SQLModel
from database import engine
from routers import address, contact, user
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


app = FastAPI()


SQLModel.metadata.create_all(engine)


app.include_router(user.router)
app.include_router(address.router)
app.include_router(contact.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )
