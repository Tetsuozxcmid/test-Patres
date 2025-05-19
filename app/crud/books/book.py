from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from schemas.book import DefaultBookSchema
from models.books.book import Book
class BookCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self,book_data: DefaultBookSchema) -> Book:
        book = Book(**book_data.model_dump())
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        
        return book
    
    
    
    
