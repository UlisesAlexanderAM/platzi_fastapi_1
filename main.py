from typing import Annotated, List

from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse

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
def get_movies() -> List[Movie]:
    return movies


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: Annotated[int, Path(ge=1, le=2000)]) -> Movie:
    movie = filter_by_id(movies, movie_id)
    return movie


@app.get("/movies/", tags=["movies"])
def get_movies_by_category(
    category: Annotated[str, Query(min_length=5, max_length=15)]
) -> List[Movie]:
    return filter_by_category(movies, category)


@app.post("/movies", tags=["movies"])
def add_movie(new_movie: Movie):
    movies.append(new_movie)
    return JSONResponse(content={"message": "Se ha registrado la pelicula"})


@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(movie_modified: Movie, movie_id: Annotated[int, Path(ge=1, le=2000)]):
    movie = filter_by_id(movies, movie_id)
    movie.title = movie_modified.title
    movie.overview = movie_modified.overview
    movie.year = movie_modified.year
    movie.rating = movie_modified.rating
    movie.category = movie_modified.category
    return JSONResponse(content={"message": "Se ha modificado la pelicula"})


@app.delete("/movies/{movie_id}", tags=["movies"])
def delete_movie(movie_id: Annotated[int, Path(ge=1, le=2000)]):
    movie = filter_by_id(movies, movie_id)
    movies.remove(movie)
    return JSONResponse(content={"message": "Se ha eliminado la pelicula"})
