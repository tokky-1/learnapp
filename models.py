from sqlalchemy import Column, Integer, String
from database import Base

class Teacher(Base):
    __tablename__ = "teachers"
    id = Column(Integer, primary_key= True, index = True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable= False)
    name = Column(String(50), nullable= False)
    subject = Column(String(50),nullable = True)



