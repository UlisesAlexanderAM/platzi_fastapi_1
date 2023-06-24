from sqlalchemy.orm import Session
from models import models, schemas


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movies_by_category(db: Session, movie_category: str):
    return db.query(models.Movie).filter(models.Movie.category == movie_category).all()


def get_all_movies(db: Session):
    return db.query(models.Movie).all()
