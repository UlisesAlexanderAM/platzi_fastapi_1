from fastapi import FastAPI

app = FastAPI()
app.title = "My application with FastAPI and Platzi"
app.version = "0.0.1"


@app.get("/", tags=["home"])
def message():
    return "Hello world!"
