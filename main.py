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



@app.get("/", tags=["home"])
def message() -> HTMLResponse:
    return HTMLResponse("<h1>Hello world!</h1>")
