from datetime import timedelta
from typing import Annotated, Any

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from data import movies, fake_users_db
from filters import filter_by_category, filter_by_id
from models import BaseMovie, MovieWithId, Token, User
from security import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_active_user,
)

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"


@app.get("/", tags=["home"], status_code=status.HTTP_200_OK)
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.post("/token", response_model=Token)
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
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get(
    path="/movies",
    tags=["movies"],
    status_code=status.HTTP_200_OK,
)
def get_movies(
    current_user: Annotated[User, Depends(get_current_active_user)]
) -> list[MovieWithId]:
    return movies


@app.post("/movies", tags=["movies"], status_code=status.HTTP_201_CREATED)
def add_movie(
    new_movie: Annotated[
        MovieWithId,
        Body(
            title="Request body",
            description="Request body with the movie to add",
            embed=True,
        ),
    ]
) -> JSONResponse:
    movies.append(new_movie)
    return JSONResponse(content={"message": "Se ha registrado la película"})


@app.get("/movies/", tags=["movies"], status_code=status.HTTP_200_OK)
def get_movies_by_category(
    category: Annotated[
        str,
        Query(
            title="Query string",
            description="Query string with the category of movies to search",
            min_length=5,
            max_length=15,
        ),
    ]
) -> list[MovieWithId]:
    return filter_by_category(movies, category)


@app.get("/movies/{movie_id}", tags=["movies"], status_code=status.HTTP_200_OK)
def get_movie(
    movie_id: Annotated[int, Path(title="ID of the movie to get", ge=1, le=2000)]
) -> Any:
    try:
        movie = filter_by_id(movies, movie_id)
    except StopIteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pelicula con ID {movie_id} no encontrada",
        ) from None
    return movie


@app.put("/movies/{movie_id}", tags=["movies"], status_code=status.HTTP_200_OK)
def update_movie(
    movie_modified: Annotated[
        BaseMovie,
        Body(
            title="Request body",
            description="Request body with the data to modified of movie",
            embed=True,
        ),
    ],
    movie_id: Annotated[int, Path(title="ID of the movie to modified", ge=1, le=2000)],
) -> JSONResponse:
    try:
        movie = filter_by_id(movies, movie_id)
    except StopIteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Película con ID {movie_id} no encontrada",
        ) from None
    movie.title = movie_modified.title
    movie.overview = movie_modified.overview
    movie.year = movie_modified.year
    movie.rating = movie_modified.rating
    movie.category = movie_modified.category
    return JSONResponse(content={"message": "Se ha modificado la película"})


@app.delete("/movies/{movie_id}", tags=["movies"], status_code=status.HTTP_200_OK)
def delete_movie(
    movie_id: Annotated[int, Path(title="ID of the movie to delete", ge=1, le=2000)]
) -> JSONResponse:
    try:
        movie = filter_by_id(movies, movie_id)
    except StopIteration:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pelicula con ID {movie_id} no encontrada",
        ) from None
    movies.remove(movie)
    return JSONResponse(content={"message": "Se ha eliminado la película"})
