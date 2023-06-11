def filter_by_id(movies_list: list, movie_id: int) -> dict:
    movie = next(filter(lambda movies: movies["id"] == movie_id, movies_list))
    return movie


def filter_by_category(movies_list: list, movie_category) -> list:
    return list(
        filter(lambda movies: movies["category"] == movie_category, movies_list)
    )
