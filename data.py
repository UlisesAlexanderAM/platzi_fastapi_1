from models import MovieWithId

movies: list[MovieWithId] = [
    BaseMovie(
        id=1,
        title="Avatar",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year=2009,
        rating=7.8,
        category="Acción",
    )
]
