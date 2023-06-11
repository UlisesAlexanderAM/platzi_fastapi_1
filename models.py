from pydantic import BaseModel, Field
from typing import Optional


class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=0.0, le=10.0)
    category: str = Field(min_lengt=5, max_lengt=15)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Titulo de la pelicula",
                "overview": "Descripcion de la pelicula",
                "year": 2022,
                "rating": 6.5,
                "category": "Acción",
            }
        }
