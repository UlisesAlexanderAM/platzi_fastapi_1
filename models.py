from pydantic import BaseModel, EmailStr, Field


class BaseMovie(BaseModel):
    title: str = Field(description="Title of the movie", min_length=5, max_length=30)
    overview: str = Field(
        description="Overview of the movie", min_length=15, max_length=150
    )
    year: int = Field(description="The year the movie was released", le=2022)
    rating: float = Field(description="The rating given to the movie", ge=0.0, le=10.0)
    category: str = Field(
        description="Category of the movie", min_length=5, max_length=15
    )

    class Config:
        schema_extra = {
            "example": {
                "title": "Titulo de la película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 6.5,
                "category": "Acción",
            }
        }


class MovieWithId(BaseMovie):
    id: int = Field(description="The ID of the movie")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo de la película",
                "overview": "Descripción de la película",
                "year": 2022,
                "rating": 6.5,
                "category": "Acción",
            }
        }


class User(BaseModel):
    email: EmailStr = Field(description="User's login email")
    password: str = Field(description="User's login password")
