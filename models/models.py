from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class Movie(BaseModel):
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


class User(BaseModel):
    username: str
    email: EmailStr = Field(description="User's login email")
    disabled: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(User):
    hashed_password: str
