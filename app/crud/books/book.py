from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from schemas.book import DefaultBookSchema, BookUpdate
from models.books.book import Book
from sqlalchemy import select


class BookCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all_books(self):
        result = await self.db.execute(select(Book))
        books = result.scalars().all()
        return books

    async def create_book(self, book_data: DefaultBookSchema) -> Book:
        book = Book(**book_data.model_dump())
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)

        return book

    async def update_book(self, book_data: BookUpdate, book_id: int) -> Book:
        result = await self.db.execute(select(Book).where(book_id == Book.id))
        book = result.scalars().first()
        if not book:
            raise ValueError("book not found")

        for key, value in book_data.model_dump().items():
            setattr(book, key, value)
            await self.db.commit()
            await self.db.refresh(book)

        return book

    async def delete_book(self, book_id: int) -> bool:
        result = await self.db.execute(select(Book).where(Book.id == book_id))
        book = result.scalars().first()

        if not book:
            return False

        await self.db.delete(book)
        await self.db.commit()

        return True
