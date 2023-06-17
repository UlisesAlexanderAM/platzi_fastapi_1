from typing import Annotated, Any

from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

from data import movies
from filters import filter_by_category, filter_by_id
from jwt_manager import create_token, validate_token
from models import BaseMovie, MovieWithId, User

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")


@app.get("/", tags=["home"], status_code=status.HTTP_200_OK)
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
        return token


@app.get(
    "/movies",
    tags=["movies"],
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_200_OK,
)
def get_movies() -> list[MovieWithId]:
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
