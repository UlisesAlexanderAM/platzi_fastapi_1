from typing import Annotated, Any

from fastapi import APIRouter, Body, Depends, HTTPException, Path, Query, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.dependencies import get_db
from app.models import schemas
from app.security import get_current_active_user

router = APIRouter(
    prefix="/movies",
    tags=["movies"],
    responses={404: {"description": "Movie not found"}},
)


@router.get(
    path="/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Movie],
)
def get_movies(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Any:
    return jsonable_encoder(crud.get_all_movies(db))


@router.post("/movies", status_code=status.HTTP_201_CREATED)
def add_movie(
    new_movie: Annotated[
        schemas.MovieBase,
        Body(
            title="Request body",
            description="Request body with the movie to add",
            embed=True,
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
):
    movie_added = crud.add_movie(db, new_movie)
    return f"Se ha registrado la película: {jsonable_encoder(movie_added)}"


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.Movie],
)
def get_movies_by_category(
    category: Annotated[
        str,
        Query(
            title="Query string",
            description="Query string with the category of movies to search",
            min_length=5,
            max_length=15,
        ),
    ],
    db: Annotated[Session, Depends(get_db)],
) -> Any:
    movies = crud.get_movies_by_category(db, category)
    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron peliculas de la categoria: {category}.",
        )
    return jsonable_encoder(movies)


@router.get(
    "/{movie_id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.Movie,
)
def get_movie(
    movie_id: Annotated[int, Path(title="ID of the movie to get", ge=1, le=2000)],
    db: Annotated[Session, Depends(get_db)],
) -> Any:
    movie = crud.get_movie_by_id(db, movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la película con ID: {movie_id}.",
        )
    return movie


@router.put("/{movie_id}", status_code=status.HTTP_200_OK)
def update_movie(
    movie_modified: Annotated[
        schemas.MovieBase,
        Body(
            title="Request body",
            description="Request body with the data to modified of movie",
            embed=True,
        ),
    ],
    movie_id: Annotated[int, Path(title="ID of the movie to modified", ge=1, le=2000)],
    db: Annotated[Session, Depends(get_db)],
):
    movie_updated = crud.update_movie(db, movie_id, movie_modified)
    return f"Se ha modificado la película {jsonable_encoder(movie_updated)}"


@router.delete("/{movie_id}", status_code=status.HTTP_200_OK)
def delete_movie(
    movie_id: Annotated[int, Path(title="ID of the movie to delete", ge=1, le=2000)],
    db: Annotated[Session, Depends(get_db)],
):
    movie = crud.delete_movie(db, movie_id)
    return f"Se ha eliminado la película {jsonable_encoder(movie)}"
