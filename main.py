from typing import Annotated, Any, List

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer

from models import Movie, User
from data import movies
from filters import filter_by_id, filter_by_category
from jwt_manager import create_token, validate_token

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"


class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data["email"] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales invalidas")


@app.get("/", tags=["home"])
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token = create_token(user.dict())
    return token


@app.get("/movies", tags=["movies"], dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return movies


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: Annotated[int, Path(ge=1, le=2000)]) -> Any:
    try:
        movie = filter_by_id(movies, movie_id)
    except StopIteration:
        return JSONResponse(
            content={"message": "Could not find"}, status_code=status.HTTP_404_NOT_FOUND
        )
    return movie


@app.get("/movies/", tags=["movies"])
def get_movies_by_category(
    category: Annotated[str, Query(min_length=5, max_length=15)]
) -> List[Movie]:
    return filter_by_category(movies, category)


@app.post("/movies", tags=["movies"])
def add_movie(new_movie: Movie) -> JSONResponse:
    movies.append(new_movie)
    return JSONResponse(content={"message": "Se ha registrado la película"})


@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(
    movie_modified: Movie, movie_id: Annotated[int, Path(ge=1, le=2000)]
) -> JSONResponse:
    movie = filter_by_id(movies, movie_id)
    movie.title = movie_modified.title
    movie.overview = movie_modified.overview
    movie.year = movie_modified.year
    movie.rating = movie_modified.rating
    movie.category = movie_modified.category
    return JSONResponse(content={"message": "Se ha modificado la película"})


@app.delete("/movies/{movie_id}", tags=["movies"])
def delete_movie(movie_id: Annotated[int, Path(ge=1, le=2000)]) -> JSONResponse:
    movie = filter_by_id(movies, movie_id)
    movies.remove(movie)
    return JSONResponse(content={"message": "Se ha eliminado la película"})
