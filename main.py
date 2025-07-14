from fastapi import FastAPI,HTTPException,status,Depends, requests,Request,Response,UploadFile,File
from sqlalchemy.orm import Session
from routes import studentroutes,teacherroutes ,experiment,fileroutes
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from database.connector import get_db
from  database.model import Student
from auth.cipher import verifyhash,create_token,get_user
from auth.authmodel import Token
from middleware import ratelimit
import time

app = FastAPI(
    title="LEARNAPP",
    description="beginner project",
    version="1.0.0")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
token: str = Depends(oauth2_scheme)
headers = {
    "Authorization": f"Bearer {token}"
}

#app.add_middleware(ratelimit)
app.include_router(fileroutes.filerouter,tags=["Files"])
app.include_router(teacherroutes.teacherRouter,tags =["teachers"] )
app.include_router(studentroutes.studentRouter,tags =["students"] )



@app.middleware('HTTP')
async def measure_time(request : Request ,call_next):
    start_time = time.time()
    responce = await call_next(request)
    processtime = time.time() - start_time
    processtime=str(processtime)
    responce.headers["X-Process-speed"]=processtime
    return responce

def verify_user(username:str,password:str,db:Session = Depends(get_db)):
    user = db.query(Student).filter(Student.username == username).first()
    if user:
        hash = verifyhash(password,user.password)
        if not hash:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credentials")
        return user 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid user")


@app.post("/token")#,response_model=Token)
async def give_token(formdata:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(get_db)):
    user = verify_user(formdata.username,formdata.password,db = db )
    if user:
        access_token = create_token(data = {"sub": user.username})
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    return "user not found"
        

@app.get("/verify_user")
async def curent_user(user:Student = Depends(get_user)):
    return user


@app.post("/login")
async def login(user = Depends(oauth2_scheme)):
    return "blank"
    


app.include_router(experiment.experimentroute,tags=["testing"])

@app.get("/ping")
def ping(token: str = Depends(oauth2_scheme)):
    return {"token_received": token}

