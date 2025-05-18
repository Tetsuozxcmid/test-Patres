from core.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String
from typing import List, Optional,TYPE_CHECKING


if TYPE_CHECKING:
    from models.library.borrowed import BorrowedBook

class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    title: Mapped[str] = mapped_column(String(30))
    author: Mapped[str] = mapped_column(String(60))
    publication_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    isbn: Mapped[Optional[str]] = mapped_column(String(13), unique=True, nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    borrow_records: Mapped[List["BorrowedBook"]] = relationship(back_populates="book")