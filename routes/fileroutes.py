from fastapi import APIRouter,status,HTTPException,Depends,UploadFile,File,Response
from sqlalchemy.orm import Session
from database.connector import get_db
from database.crud import accept_file,get_all_files,get_by_id
from fastapi.responses import JSONResponse

filerouter =  APIRouter(prefix="/files")
DB : Session = Depends(get_db)
ALLOWED_FILE_TYPES = ["image/png","image/jpeg"]

@filerouter.post("/basic_upload")
async def upload_file(file: UploadFile = File ()):
    await file.read()
    return {
        "filename" : file.filename,
        "content type": file.content_type 
    }

@filerouter.post("/uploadToDB")
async def toDB(file: UploadFile = File(),db: Session = Depends(get_db)):
    return await accept_file( file = file, db = db)

@filerouter.post("/multiple_upload")
async def multiple_upload(db = DB ,file:list [UploadFile] = File() ):
    file_details = []   
    for item in file:
        file_details.append( await accept_file(file= item,db = db))
    return file_details

@filerouter.post("/profile_pic")
async def profile(pic:UploadFile = File(),db = DB):
    print(pic.content_type)
    if pic.content_type not in ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return await accept_file(file=pic,db = db )

@filerouter.post("/file_size")
async def file(file:UploadFile = File(),db = DB):
    limit = 10 *1024*1024
    if file.size >= limit :
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
    return await accept_file(file=file,db = db )


@filerouter.get("/files")
def get_all_Files(db:Session = Depends(get_db)):
   return get_all_files(db = db)
   

@filerouter.get("/by-id/{id}")
def get_file_by_id(id = id,db:Session = Depends(get_db)):
    return get_by_id(db = db,id=id )
    







#upload ,delete,get files