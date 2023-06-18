from config.database import Session
from models.movie_db import MovieDB


def filter_by_id(movie_id: int) -> MovieDB:
    db = Session()
    return db.query(MovieDB).filter(MovieDB.id == movie_id).first()


def filter_by_category(movie_category: str) -> list[MovieDB]:
    db = Session()
    return db.query(MovieDB).filter(MovieDB.category == movie_category).all()
