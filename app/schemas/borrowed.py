import datetime
from pydantic import BaseModel, Field
from typing import Optional


class BorrowBase(BaseModel):
    book_id: int
    reader_id: int


class BorrowCreate(BorrowBase):
    pass


class BorrowUpdate(BaseModel):
    return_date: datetime.datetime = datetime.datetime.now()
    book_id: int
