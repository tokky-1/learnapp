from fastapi import APIRouter,status,HTTPException,Depends
from sqlalchemy.orm import Session 
from models.studentmodel import createStudentModel as CS,updateStudentModel as SUM
from database.crud import create_student,get_all_students,get_by_id,delete_student,edit_student
from database.connector import get_db
from database.model import Student
from auth.cipher import verifyhash,createhash

studentRouter = APIRouter(prefix="/student")

@studentRouter.get("/students")
def getStudents(db:Session = Depends(get_db)):
   return get_all_students(db = db)
   

@studentRouter.get("/by-id/{id}")
def get_student_by_id(id = id,db:Session = Depends(get_db)):
    return get_by_id(db = db,id=id )
    
@studentRouter.post("/createStudent",status_code=status.HTTP_201_CREATED)
async def create_new_student(student : CS,db:Session = Depends(get_db)):
    hashedpassword = createhash(student.password)
    return create_student(db = db,uname = student.username,grade=student.grade,pword = hashedpassword,email=student.email)

@studentRouter.delete("/delete/{name}",status_code=status.HTTP_204_NO_CONTENT)
def delete_named_student(name ,db:Session = Depends(get_db)):
   return delete_student(db=db, db_user= name)
            
@studentRouter.patch("/update")
def update_student(student:SUM,id = id ,db:Session = Depends(get_db)):
    return edit_student(db=db,id =id, update= student)
   
@studentRouter.post("/SignIn",status_code=status.HTTP_200_OK)
async def sign_in(username:str,password:str , db:Session = Depends(get_db)):
    student = db.query(Student).filter(Student.username == username).first()
    if student:
        return student.password == password

@studentRouter.post("/verifyauth",status_code=status.HTTP_200_OK)
async def log_in(username:str,password:str , db:Session = Depends(get_db)): 
    student = db.query(Student).filter(Student.username == username).first()
    if student:
        is_hashed = verifyhash(plainpassword=password, hashedpassword=student.password)
        return is_hashed
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

