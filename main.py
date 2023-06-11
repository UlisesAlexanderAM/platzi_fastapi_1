from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"

movies: list[dict] = [
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": 2009,
        "rating": 7.8,
        "category": "Acción",
    }
]


class Movie(BaseModel):
    id: int
    title: str
    overview: str
    year: int
    rating: float
    category: str


class MovieWithoutId(BaseModel):
    title: str
    overview: str
    year: int
    rating: float
    category: str


def filter_by_id(movies_list: list, movie_id: int) -> list:
    return list(filter(lambda movies: movies["id"] == movie_id, movies_list))


def filter_by_category(movies_list: list, movie_category) -> list:
    return list(
        filter(lambda movies: movies["category"] == movie_category, movies_list)
    )


@app.get("/", tags=["home"])
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")


@app.get("/movies", tags=["movies"])
def get_movies() -> list:
    return movies


@app.get("/movies/{movie_id}", tags=["movies"])
def get_movie(movie_id: int) -> dict:
    movie = filter_by_id(movies, movie_id)
    if len(movie) == 0:
        raise HTTPException(
            status_code=404, detail=f"Movie with id = {movie_id} not found"
        )
    return movie[0]


@app.get("/movies", tags=["movies"])
def get_movies_by_category(category: str) -> list:
    return filter_by_category(movies, category)


@app.post("/movies", tags=["movies"])
def add_movie(new_movie: Movie):
    movies.append(new_movie.dict())
    return movies


@app.put("/movies/{movie_id}", tags=["movies"])
def update_movie(movie_id: int, movie_modified: MovieWithoutId):
    for movie in movies:
        if movie.get("id") == movie_id:
            movie.update(movie_modified)
    return movies
