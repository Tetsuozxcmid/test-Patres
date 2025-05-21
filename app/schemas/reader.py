
from pydantic import BaseModel,Field, EmailStr
from typing import Optional

class DefaultReaderSchema(BaseModel):
    
    name: str = Field(...,min_length=6,max_length=60,example="nakanakanakana")
    email: EmailStr = Field(...,min_length=2,max_length=40,example="tetsuonakamura6@gmail.com")
    
    

class ReaderUpdate(BaseModel):
    name: Optional[str] = Field(...,min_length=6,max_length=60,example="nakanakanakana")
    email: Optional[EmailStr] = Field(...,min_length=2,max_length=40,example="tetsuonakamura6@gmail.com")
    
    
