from sqlalchemy.orm import Session
from models.models import MovieDB


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(MovieDB).filter(MovieDB.id == movie_id).first()


def get_movies_by_category(db: Session, movie_category: str):
    return db.query(MovieDB).filter(MovieDB.category == movie_category).all()


def get_all_movies(db: Session):
    return db.query(MovieDB).all()
