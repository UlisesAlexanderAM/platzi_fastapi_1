from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=30)
    overview: str = Field(min_length=15, max_length=150)
    year: int = Field(le=2022)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_length=5, max_length=15)

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
    email: EmailStr
    password: str
