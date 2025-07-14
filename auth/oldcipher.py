#creating and verifying hash
from passlib.context import CryptContext
from jose import jwt ,JWTError
from fastapi.security import OAuth2PasswordBearer
import time
from datetime import datetime, timedelta 
from fastapi import HTTPException,status,Depends

ALGORITHIM = "HS256"
SECRET_KEY = "ayoajayioluwatokiloba1"
EXPIRE = 3600

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
hashcontext = CryptContext(schemes=["bcrypt"])# check other encruption methods

def createhash(password:str):
        return hashcontext.hash(password)

def verifyhash(plainpassword:str,hashedpassword:str):
        return hashcontext.verify(plainpassword,hashedpassword)
    #compares the 2 hashes

#take the data(dict)
def create_token(data:dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=EXPIRE)
    payload.update({"exp":expire})
    token = jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHIM)
    return token

# #input expiry time
# def verify_token(token):
#        payload =  jwt.decode(token,SECRET_KEY,algorithms=ALGORITHIM) #alogorithim meant to be a list as in in these[]
#       # print(type(payload))
#        if time.time() > payload.get("exp"):
#               raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="token expired")
#        return payload
   
# #erify_token("eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJsb2FkIiwiZXhwIjozMH0.FomZiJb2abaWfqXR9ZOk4hY29fNzBNfWTD5SfrXng9w")
def verify_token(token: str):
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHIM])
        if time.time() > payload.get("exp"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        return payload
    except JWTError:
        print(token)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token")
    
def get_user(token: str = Depends(oauth2_scheme)):
    print(f"token is { token}" )
    payload = verify_token(token)
    user = payload.get("sub")
    print(user)
    return user