from datetime import datetime
from typing import Dict, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from schemas.borrowed import BorrowCreate, BorrowUpdate
from models.library.borrowed import BorrowedBook


class BorrowCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_borrow(self, book_id: int, reader_id: int) -> BorrowedBook:
        exists = await self.db.execute(
            select(BorrowedBook)
            .where(BorrowedBook.book_id == book_id)
            .where(BorrowedBook.return_date == None)
        )
        if exists.scalars().first():
            raise ValueError("Книга уже занята")

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

    async def update_borrow_note(self, reader_id: int, borrow_data: BorrowUpdate) -> BorrowedBook:

        result = await self.db.execute(
            select(BorrowedBook)
            .where(BorrowedBook.reader_id == reader_id)
            .where(BorrowedBook.return_date == None)
        )
        borrowed = result.scalars().first()

        if not borrowed:
            raise ValueError("Активная запись о взятии книги не найдена")

        update_data = borrow_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(borrowed, key, value)

        await self.db.commit()
        await self.db.refresh(borrowed)

        return borrowed

    async def delete_borrowed_note(self, borrow_id: int)-> bool:
        result = await self.db.execute(select(BorrowedBook).where(BorrowedBook.id == borrow_id))
        borrowed_to_del = result.scalars().first()

        await self.db.delete(borrowed_to_del)
        await self.db.commit()

        return True
