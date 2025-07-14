from fastapi import  UploadFile, File,HTTPException,status
from sqlalchemy.orm import Session 
from .model import Student,Teacher,Files

#create student
def create_student(db:Session,uname:str,email:str,grade:str,pword:str):
    db_student = Student(username = uname,email = email,grade = grade,password = pword) 
    try:
        db.add(db_student)
        db.commit()
        db.refresh(db_student)
    except Exception as e : 
        db.rollback()
        raise e  
    finally: 
        db.close()

    return db_student  


#get all student
def get_all_students(db:Session):
    return db.query(Student).all()
    
#get by id
def get_by_id(db:Session,id:int):
    return db.query(Student).filter(Student.id == id ).first()

#edit/update student
def edit_student(db:Session,id:int,update):
    db_student = db.query(Student).filter(Student.id == id).first()
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for field,value in update.dict(exclude_unset = True).items():
        setattr(db_student,field,value)
    db.commit()
    db.add(db_student)
  
    return db_student

#delete student
def delete_student(db:Session,db_user:str):
    exist = db.query(Student).filter(Student.username == db_user ).first()
    if exist :
        db.delete(exist)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

#create teacher
def create_teacher(db:Session,uname:str,email:str,grade:str,pword:str):
    db_teacher = Teacher(username = uname,email = email,grade = grade,password = pword) 
    try:
        db.add(db_teacher)
        db.commit()
        db.refresh(db_teacher)
    except Exception as e : 
        db.rollback()
        raise e  
    finally: 
        db.close()

    return db_teacher  
#get all teacher
def get_all_teachers(db:Session):
    return db.query(Teacher).all()
   
#get by id
def get_by_id(db:Session,id:int):
    return db.query(Teacher).filter(Teacher.id == id ).first()

#edit/update teacher
def edit_teacher(db:Session,id:int,update):  
    db_teacher = db.query(Teacher).filter(Teacher.id == id).first()
    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    for field,value in update.dict(exclude_unset = True).items():
        setattr(db_teacher,field,value)

    db.commit()
    db.add(db_teacher)
    
    return db_teacher

#delete teacher
def delete_teacher(db:Session,db_user:str):
    exist = db.query(Teacher).filter(Teacher.username == db_user ).first()
    if exist :
        db.delete(exist)
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    return "user doesn't exist"

# upload materials
async def accept_file( db:Session,file: UploadFile = File(...)):
    datum = await file.read()
    
    record = Files(
        #user_id = user_id,
        filename=file.filename,
        type=file.content_type,
        size = str(len(datum)),
        file=datum
    )
    try:
        db.add(record)
        db.commit()
        db.refresh(record)

        return {
            "id": record.file_id,
            "filename": record.filename,
            "content type": record.type,
            "size": record.size,
            "uploaded_at": record.uploaded_at
        }
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    #get all teacher
def get_all_files(db:Session):
    record =  db.query(Files).all()
    for item in record:
        return{ 
            "id": item.file_id,
            "filename": item.filename,
            "content_type": item.type,
            "size": item.size,
            "uploaded_at": item.uploaded_at
        }
    
#get by id
def get_by_id(db:Session,id:int):
    file_record = db.query(Files).filter(Files.file_id == id ).first()
    if not file_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="file doesn't exist")
    return{ 
         "id": file_record.file_id,
        "filename": file_record.filename,
        "content_type": file_record.type,
        "size": file_record.size,
        "uploaded_at": file_record.uploaded_at
    }