from typing import Dict

from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from schemas.reader import DefaultReaderSchema
from models.users.reader import Reader

class ReaderCRUD:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_reader(self,user_data: DefaultReaderSchema) -> Reader:
        reader = Reader(**user_data.model_dump())
        self.db.add(reader)
        await self.db.commit()
        await self.db.refresh(reader)
        
        return reader