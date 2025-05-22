
from __future__ import annotations
from typing import List, TYPE_CHECKING
from core.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String

if TYPE_CHECKING:
    from models.library.borrowed import BorrowedBook


class Reader(Base):
    __tablename__ = "readers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False)

    borrowed_books: Mapped[List["BorrowedBook"]] = relationship(
        "BorrowedBook", back_populates="reader")
