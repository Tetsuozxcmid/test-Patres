from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db import get_db
from schemas.book import DefaultBookSchema, BookUpdate
from models.books.book import Book
from models.admin.librarian import librarian
from crud.books.book import BookCRUD
from api.v1.admins.auth import get_current_user

router = APIRouter(prefix="/books", tags=["books interactions"])


@router.get('/all_books')
async def get_books(db: AsyncSession = Depends(get_db)):
    crud = BookCRUD(db)

    return await crud.get_all_books()


@router.post('/load_book')
async def load_book(book_data: DefaultBookSchema, current_user: librarian = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    crud = BookCRUD(db)

    return await crud.create_book(book_data)


@router.patch('/update_book')
async def update_book(book_data: DefaultBookSchema, book_id: int, current_user: librarian = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    crud = BookCRUD(db)
    return await crud.update_book(book_data, book_id)


@router.delete('/delete_book')
async def delete_book(book_id: int, current_user: librarian = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    crud = BookCRUD(db)
    return await crud.delete_book(book_id)
