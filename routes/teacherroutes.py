from fastapi import APIRouter,status,HTTPException,Depends,UploadFile,File
from sqlalchemy.orm import Session 
from database.crud import create_teacher,get_all_teachers,get_by_teacher_id,delete_teacher,edit_teacher,accept_file
from database.connector import get_db
from models.teachermodel import createteacherModel as CT,updateTeacherModel as UTM
from auth.cipher import createhash,verifyhash
from database.model import Teacher


teacherRouter = APIRouter(prefix="/teacher")

@teacherRouter.get("/teachers")
def getTeachers(db:Session = Depends(get_db)):
   return get_all_teachers(db = db)
   

@teacherRouter.get("/by-id/{id}")
def get_teacher_by_id(id = id,db:Session = Depends(get_db)):
    return get_by_teacher_id(db = db,id=id )
    
@teacherRouter.post("/createTeacher",status_code=status.HTTP_201_CREATED)
async def create_new_teacher(teacher : CT,db:Session = Depends(get_db) ):
    hashedpassword = createhash(teacher.password)
    return create_teacher(db = db,uname = teacher.username,email= teacher.email,grade=teacher.grade,pword =hashedpassword)

@teacherRouter.delete("/delete/{name}",status_code=status.HTTP_204_NO_CONTENT)
def delete_named_teacher(name ,db:Session = Depends(get_db)):
   return delete_teacher(db=db, db_user= name)

@teacherRouter.patch("/update")
def update_teacher(teacher:UTM,id = id,db:Session = Depends(get_db)):
    return edit_teacher(db=db,id=id, update= teacher)

@teacherRouter.post("/verifyauth",status_code=status.HTTP_200_OK)
async def log_in(username:str,password:str , db:Session = Depends(get_db)): 
    teacher = db.query(Teacher).filter(Teacher.username == username).first()
    if teacher:
        verifyhash(plainpassword=password, hashedpassword=teacher.password)
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@teacherRouter.patch("/upload")
async def upload_doc(doc:UploadFile = File ,db:Session = Depends(get_db)):
    return await accept_file(file = doc ,db = db)