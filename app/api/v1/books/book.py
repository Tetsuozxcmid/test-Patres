from fastapi import APIRouter, Depends,Request,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db import get_db
from schemas.book import DefaultBookSchema
from models.books.book import Book
from crud.books.book import BookCRUD

router = APIRouter(prefix="/books", tags=["books interactions"])

@router.post('/load_book')
async def load_book(book_data: DefaultBookSchema,db: AsyncSession = Depends(get_db)):
    crud = BookCRUD(db)

    return await crud.create_book(book_data)