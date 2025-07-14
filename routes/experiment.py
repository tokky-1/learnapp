from fastapi.security import HTTPBasic,HTTPBasicCredentials
from fastapi import Depends,HTTPException,status,APIRouter
from sqlalchemy.orm import Session
from database.connector import get_db
from database.model import Student

security = HTTPBasic()
experimentroute= APIRouter()

def login( 
          db:Session = Depends(get_db), credential:HTTPBasicCredentials = Depends(security)
    ):
    user = db.query(Student).filter(Student.username==credential.username).first()
    if user and user.password == credential.password:
               return user
           #raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

@experimentroute.put("/test")
def testing( user = Depends(login)):
    return "you are in "

@experimentroute.delete("/test")
def testing2( user = Depends(login)):
    return "deleted "

