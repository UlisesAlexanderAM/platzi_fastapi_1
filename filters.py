from typing import List

from models import Movie


def filter_by_id(movies_list: List[Movie], movie_id: int) -> Movie:
    movie = next(filter(lambda movies: movies.id == movie_id, movies_list))
    return movie


def filter_by_category(movies_list: List[Movie], movie_category: str) -> List[Movie]:
    return list(filter(lambda movies: movies.category == movie_category, movies_list))
