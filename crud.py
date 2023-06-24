from config.database import Session
from models.models import MovieDB


def get_movie_by_id(movie_id: int):
    db = Session()
    return db.query(MovieDB).filter(MovieDB.id == movie_id).first()


def get_movies_by_category(movie_category: str):
    db = Session()
    return db.query(MovieDB).filter(MovieDB.category == movie_category).all()


def get_all_movies():
    db = Session()
    return db.query(MovieDB).all()
