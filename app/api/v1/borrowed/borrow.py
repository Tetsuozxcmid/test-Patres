from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.db import get_db
from schemas.borrowed import BorrowCreate,BorrowUpdate
from models.books.book import Book
from models.admin.librarian import librarian
from crud.borrowed.borrow import BorrowCRUD
from api.v1.admins.auth import get_current_user

router = APIRouter(prefix="/borrowed", tags=["borrowed interactions"])


@router.post('/load_note')
async def load_note(
    book_id: int,
    reader_id: int,
    current_user: librarian = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    crud = BorrowCRUD(db)
    return await crud.create_borrow(book_id, reader_id)

@router.get('/get_borrowed')
async def get_borrowed_notes(
    reader_id: int,
    current_user: librarian = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    crud = BorrowCRUD(db)
    return await crud.get_borrowed_books(reader_id)

@router.patch('/update_borrow_note/{reader_id}',description = "returned note")
async def update_note(
    reader_id: int,
    book_id: int,
    borrow_data: BorrowUpdate,
    current_user: librarian = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    crud = BorrowCRUD(db)
    
    return await crud.update_borrow_note(reader_id,book_id, borrow_data)
    
        
@router.delete('/delete_borrowed_note/{borrow_id}')
async def delete_note(borrow_id: int,current_user: librarian = Depends(get_current_user),db: AsyncSession = Depends(get_db)):
    crud = BorrowCRUD(db)
    return await crud.delete_borrowed_note(borrow_id)
    
