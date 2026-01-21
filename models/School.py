from sqlalchemy import Column,Integer,String,DateTime
from database.data import Base


class School(Base):
    __tablename__ = 'school'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    founding_date = Column(DateTime)
    address = Column(String)
    city = Column(String)

