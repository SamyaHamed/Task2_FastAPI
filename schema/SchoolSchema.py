from pydantic import BaseModel
from datetime import datetime

from schema.StudentSchema import StudentResponse


class SchoolCreate(BaseModel):
    name: str
    founding_date: datetime
    address: str
    city: str

class SchoolResponse(BaseModel):
    id: int
    name: str
    founding_date: datetime
    address: str
    city: str

class SchoolWithStudents(BaseModel):
    name: str
    students: list[StudentResponse]

    class Config:
        orm_mode = True



