from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models import models, schemas


def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def get_movies_by_category(db: Session, movie_category: str):
    return db.query(models.Movie).filter(models.Movie.category == movie_category).all()


def get_all_movies(db: Session):
    return db.query(models.Movie).all()


def add_movie(db: Session, movie: schemas.MovieBase):
    db_movie = models.Movie(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def update_movie(db: Session, movie_id: int, modified_movie: schemas.MovieBase):
    db_movie: models.Movie = get_movie_by_id(db, movie_id)
    if not db_movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la película con ID: {movie_id}.",
        )
    for var, value in vars(modified_movie).items():
        setattr(db_movie, var, value) if value else None
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
