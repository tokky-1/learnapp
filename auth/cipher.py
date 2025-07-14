import time
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from database.model import Student
from database.connector import get_db




SECRET_KEY ="blackcard"
ALGORITHM = "HS256"
EXPIRE =3600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
hashcontext=CryptContext(schemes=["bcrypt"])

def createhash(password:str):  
    return hashcontext.hash(password)
    
def verifyhash(plainpassword:str, hashedpassword:str):
    return hashcontext.verify(plainpassword,hashedpassword)



def create_token(data: dict):
    payload=data.copy()
    expire = datetime.utcnow() + timedelta(minutes=float(EXPIRE))
    payload.update({"exp":expire.timestamp()})
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    print(" this Received token:", token)
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    if time.time() > payload.get("exp"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
    return payload
    # except JWTError:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid token"
    #     )

def get_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print("Received token:", token)
    payload = verify_token(token)
    username = payload.get("sub")
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    user = db.query(Student).filter(Student.username == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user

