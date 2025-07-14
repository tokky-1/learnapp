from sqlalchemy import Column,String,Integer,LargeBinary,ForeignKey,DateTime,func
from .connector import engine
from sqlalchemy.ext.declarative import declarative_base 

base = declarative_base()

class Student(base): # student table in database
    __tablename__="students"
    id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    username = Column(String,unique=True )
    email = Column(String,unique=True)
    grade = Column(String,nullable=True)
    password = Column(String)

class Teacher(base): # teacher table in database
    __tablename__= "teachers"
    id = Column(Integer,autoincrement=True,primary_key=True,index=True)
    username = Column(String,unique=True )
    email = Column(String,unique=True)
    grade = Column(String,nullable=True)
    password = Column(String)

class Files(base):
    __tablename__ = "files"
    file_id = Column(Integer,autoincrement=True,primary_key=True,index=True)
   # user_id = Column(Integer,ForeignKey("teachers.id") ,index=True,nullable=True)
    filename = Column(String)
    type = Column(String)
    size = Column(String)
    file = Column(LargeBinary)
    uploaded_at  = Column(DateTime(timezone=True), server_default=func.now())

base.metadata.create_all(bind=engine) 