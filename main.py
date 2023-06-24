from datetime import timedelta
from typing import Annotated, Any

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import crud
from config.database import Base, SessionLocal, engine
from data import fake_users_db
from models import schemas
from security import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    settings,
)

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    path="/movies",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Movie],
)
def get_movies(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Any:
    return jsonable_encoder(crud.get_all_movies(db))


@app.post("/movies", tags=["movies"], status_code=status.HTTP_201_CREATED)
def add_movie(
    new_movie: Annotated[
        schemas.MovieBase,
        Body(
            title="Request body",
            description="Request body with the movie to add",
            embed=True,
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    movie_added = crud.add_movie(db, new_movie)
    return f"Se ha registrado la película: {jsonable_encoder(movie_added)}"


@app.get(
    "/movies/",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Movie],
)
def get_movies_by_category(
    category: Annotated[
        str,
        Query(
            title="Query string",
            description="Query string with the category of movies to search",
            min_length=5,
            max_length=15,
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Any:
    movies = crud.get_movies_by_category(db, category)
    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron peliculas de la categoria: {category}.",
        )
    return jsonable_encoder(movies)


@app.get(
    "/movies/{movie_id}",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
    response_model=schemas.Movie,
)
def get_movie(
    movie_id: Annotated[int, Path(title="ID of the movie to get", ge=1, le=2000)],
    db: Annotated[Session, Depends(get_db)],
) -> Any:
    movie = crud.get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la película con ID: {movie_id}.",
        )
    return movie


@app.put("/movies/{movie_id}", tags=["movies"], status_code=status.HTTP_200_OK)
def update_movie(
    movie_modified: Annotated[
        schemas.MovieBase,
        Body(
            title="Request body",
            description="Request body with the data to modified of movie",
            embed=True,
        ),
    ],
    movie_id: Annotated[int, Path(title="ID of the movie to modified", ge=1, le=2000)],
    db: Annotated[Session, Depends(get_db)],
):
    movie_updated = crud.update_movie(db, movie_id, movie_modified)
    return f"Se ha modificado la película {jsonable_encoder(movie_updated)}"


@app.delete("/movies/{movie_id}", tags=["movies"], status_code=status.HTTP_200_OK)
def delete_movie(
    movie_id: Annotated[int, Path(title="ID of the movie to delete", ge=1, le=2000)],
    db: Annotated[Session, Depends(get_db)],
):
    movie = crud.delete_movie(db, movie_id)
    return f"Se ha eliminado la película {jsonable_encoder(movie)}"
