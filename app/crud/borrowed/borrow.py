from datetime import datetime
from typing import Dict, Optional

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count
from models.books.book import Book
from core.config import settings
from schemas.borrowed import BorrowCreate, BorrowUpdate
from models.library.borrowed import BorrowedBook


class BorrowCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_borrow(self, book_id: int, reader_id: int) -> BorrowedBook:
        book = await self.db.get(Book, book_id)
        active_borrows_count = await self.db.execute(
            select(count(BorrowedBook.id))
            .where(BorrowedBook.book_id == book_id)
            .where(BorrowedBook.return_date == None)
        )
        active_borrows_count = active_borrows_count.scalar()

        if book.quantity <= 0:
            raise ValueError("Книги закончились")

        active_borrows = await self.get_borrowed_books(reader_id)
        if len(active_borrows) >= 3:
            raise ValueError(
                "Пользователь уже взял 3 книги, верните хотя бы 1, что бы взять еще")

        book.quantity -= 1
        borrowed = BorrowedBook(
            book_id=book_id,
            reader_id=reader_id,
            borrow_date=datetime.now()
        )
        self.db.add(borrowed)
        await self.db.commit()
        await self.db.refresh(borrowed)
        return borrowed

    async def get_borrowed_books(self, reader_id: Optional[int] = None):
        query = select(BorrowedBook)

        if reader_id:
            query = query.where(BorrowedBook.reader_id == reader_id)

        query = query.where(BorrowedBook.return_date == None)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_borrow_note(
    self, 
    reader_id: int, 
    book_id: int,
    borrow_data: BorrowUpdate
    ) -> BorrowedBook:
    
        result = await self.db.execute(
        select(BorrowedBook)
        .where(BorrowedBook.reader_id == reader_id)
        .where(BorrowedBook.book_id == book_id)
        .where(BorrowedBook.return_date == None)
        )
        borrowed = result.scalars().first()

        if not borrowed:
            raise HTTPException(
                status_code=404,
                detail="Активная запись о взятии этой книги не найдена для данного читателя"
            )

    
        if borrowed.return_date is not None:
            raise HTTPException(
                status_code=400,
                detail="Эта книга уже была возвращена"
            )

    
        update_data = borrow_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(borrowed, key, value)

    
        book = await self.db.get(Book, book_id)
        book.quantity += 1

        await self.db.commit()
        await self.db.refresh(borrowed)

        return borrowed

    async def delete_borrowed_note(self, borrow_id: int) -> bool:
        result = await self.db.execute(select(BorrowedBook).where(BorrowedBook.id == borrow_id))
        borrowed_to_del = result.scalars().first()

        await self.db.delete(borrowed_to_del)
        await self.db.commit()

        return True
