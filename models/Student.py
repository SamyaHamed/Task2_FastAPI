from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.data import  Base
class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True,index = True)
    first_name = Column(String,nullable=False)
    last_name = Column(String,nullable=False)
    birth_date = Column(DateTime,nullable=False)
    school_id = Column(Integer, ForeignKey("school.id"), nullable=False)
    school = relationship(
        "School",
        backref="students"
    )

