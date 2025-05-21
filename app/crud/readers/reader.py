from typing import Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from schemas.reader import DefaultReaderSchema, ReaderUpdate
from models.users.reader import Reader


class ReaderCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reader(self, user_data: DefaultReaderSchema) -> Reader:
        reader = Reader(**user_data.model_dump())
        self.db.add(reader)
        await self.db.commit()
        await self.db.refresh(reader)

        return reader

    async def get_all_readers(self):
        result = await self.db.execute(select(Reader))
        readers = result.scalars().all()
        return readers

    async def delete_reader(self, user_id: int) -> bool:
        result = await self.db.execute(select(Reader).where(Reader.id == user_id))
        reader = result.scalars().first()

        if not reader:
            return False

        await self.db.delete(reader)
        await self.db.commit()

        return True

    async def update_reader(self, user_id: int, user_data: ReaderUpdate) -> Reader:
        result = await self.db.execute(select(Reader).where(Reader.id == user_id))
        reader = result.scalars().first()

        if not reader:
            raise ValueError("Reader not found")

        update_data = user_data.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(reader, key, value)

        await self.db.commit()
        await self.db.refresh(reader)

        return reader
