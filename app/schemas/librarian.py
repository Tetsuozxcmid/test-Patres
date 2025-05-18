from pydantic import BaseModel,EmailStr,Field
from typing import Optional

from pydantic.types import SecretStr


class LibrarianAuth(BaseModel):
    password: SecretStr = Field(..., min_length=8, example="password1232305")
    email: EmailStr = Field(..., example="user@example.com")

class LibrarianRegister(BaseModel):
    password: SecretStr = Field(..., min_length=8, example="password1232305")
    email: EmailStr = Field(..., example="user@example.com")