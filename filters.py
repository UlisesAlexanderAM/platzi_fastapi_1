from models import MovieWithId


def filter_by_id(movies_list: list[MovieWithId], movie_id: int) -> MovieWithId:
    movie = next(filter(lambda movies: movies.id == movie_id, movies_list))
    return movie


def filter_by_category(
    movies_list: list[MovieWithId], movie_category: str
) -> list[MovieWithId]:
    return list(filter(lambda movies: movies.category == movie_category, movies_list))
