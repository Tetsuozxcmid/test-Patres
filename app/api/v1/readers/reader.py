from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from models.admin.librarian import librarian
from core.database.db import get_db
from schemas.reader import DefaultReaderSchema, ReaderUpdate
from api.v1.admins.auth import get_current_user
from crud.readers.reader import ReaderCRUD

router = APIRouter(prefix="/readers", tags=["readers interactions"])


@router.post('/create_reader')
async def create_reader(user_data: DefaultReaderSchema, current_user: librarian = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    crud = ReaderCRUD(db)

    return await crud.create_reader(user_data)


@router.get('/get_all_readers')
async def get_readers(current_user: librarian = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    crud = ReaderCRUD(db)
    return await crud.get_all_readers()


@router.delete('/delete_reader')
async def delete_reader(user_id: int, current_user: librarian = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    crud = ReaderCRUD(db)
    return await crud.delete_reader(user_id)


@router.patch('/update_reader/{user_id}')
async def update_reader(
    user_id: int,
    user_data: ReaderUpdate,
    current_user: librarian = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    crud = ReaderCRUD(db)
    return await crud.update_reader(user_id, user_data)
