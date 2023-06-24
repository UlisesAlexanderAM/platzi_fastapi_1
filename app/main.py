from datetime import timedelta
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm

from app.config.database import Base, engine
from app.config.security import Settings
from app.data import fake_users_db
from app.models import schemas
from app.routers import movie
from app.security import authenticate_user, create_access_token

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"
app.include_router(movie.router)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["home"], status_code=status.HTTP_200_OK)
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.post("/token", tags=["auth"], response_model=schemas.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=Settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
