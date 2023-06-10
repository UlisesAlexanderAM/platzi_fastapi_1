from fastapi import FastAPI

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

@app.get("/", tags=["home"])
def message():
    return "Hello world!"
