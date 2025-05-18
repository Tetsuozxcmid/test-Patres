from core.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer,String



class librarian(Base):
    __tablename__ = "librarians"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)