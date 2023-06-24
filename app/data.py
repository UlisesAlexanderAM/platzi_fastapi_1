from app.models.schemas import Movie, UserInDB

movies: list[Movie] = [
    Movie(
        id=1,
        title="Avatar",
        overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        year=2009,
        rating=7.8,
        category="Acción",
    )
]


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
