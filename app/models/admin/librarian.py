from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.db import get_db
from schemas.librarian import LibrarianAuth
from core.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,String,select
from api.v1.admins.passlogic import pass_settings


class librarian(Base):
    __tablename__ = "librarians"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    @classmethod
    async def check_user(cls, email: EmailStr,password: str,db: AsyncSession) -> dict:
        result = await db.execute(select(cls).where(cls.email==email))
        user = result.scalar_one_or_none()
        if not user or not pass_settings.verify_password(
            plain_password=password,
            hashed_password=user.hashed_password
        ):
            return None
        
        return {
            "id": user.id,
            "email": user.email
        }