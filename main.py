from typing import Annotated

from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse

from models import Movie
from data import movies
from filters import filter_by_id, filter_by_category

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"


@app.get("/", tags=["home"])
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.get("/movies", tags=["movies"])
def get_movies() -> list:
    return movies


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: Annotated[int, Path(ge=1, le=2000)]) -> dict:
    movie = filter_by_id(movies, movie_id)
    return movie


@app.get("/movies", tags=["movies"])
def get_movies_by_category(
    category: Annotated[str, Query(min_length=5, max_length=15)]
) -> list:
    return filter_by_category(movies, category)


@app.post("/movies", tags=["movies"])
def add_movie(new_movie: Movie):
    movies.append(new_movie.dict())
    return movies


@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(movie_modified: Movie, movie_id: Annotated[int, Path(ge=1, le=2000)]):
    movie = filter_by_id(movies, movie_id)
    movie.update(movie_modified)
    movie["id"] = movie_id
    return movies


@app.delete("/movies/{movie_id}", tags=["movies"])
def delete_movie(movie_id: Annotated[int, Path(ge=1, le=2000)]):
    movie = filter_by_id(movies, movie_id)
    movies.remove(movie)
    return movies
