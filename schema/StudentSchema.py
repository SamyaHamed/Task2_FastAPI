from datetime import datetime
from typing import Optional


from pydantic import BaseModel

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: datetime

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    birth_date: Optional[datetime] = None

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: datetime


    class Config:
        orm_mode = True