import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional


class DefaultBookSchema(BaseModel):

    title: str = Field(..., min_length=6, max_length=60,
                       example="nakanakanakana")
    author: str = Field(..., min_length=2, max_length=40,
                        example="Иванов И. И.")
    publication_year: int = Field(..., gt=0,
                                  le=datetime.datetime.now().year, example=2023)
    isbn: Optional[str] = Field(
        None, min_length=6, max_length=60, example="234322213dsqwe")
    quantity: int = Field(default=1, example=123)

    @validator('publication_year')
    def validate_publication_year(cls, v):
        current_year = datetime.datetime.now().year
        if v > current_year:
            raise ValueError(
                f"Год публикации не может быть больше {current_year}")

        if v < 0:
            raise ValueError("Год публикации не может быть отрицательным")
        return v


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=30)
    author: Optional[str] = Field(None, min_length=2, max_length=60)
    publication_year: Optional[int] = Field(
        None, gt=0, le=datetime.datetime.now().year)
    quantity: Optional[int] = Field(None, ge=0)
