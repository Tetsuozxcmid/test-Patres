
from __future__ import annotations
from core.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, ForeignKey, DateTime
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.books.book import Book
    from app.models.users.reader import Reader


class BorrowedBook(Base):
    __tablename__ = "borrowed_books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    book_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("books.id"), nullable=False)
    reader_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("readers.id"), nullable=False)
    borrow_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False)
    return_date: Mapped[Optional[datetime]
                        ] = mapped_column(DateTime, nullable=True)

    book: Mapped["Book"] = relationship(
        "Book", back_populates="borrow_records")
    reader: Mapped["Reader"] = relationship(
        "Reader", back_populates="borrowed_books")
