from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class studentModel(BaseModel): # when using model object is always a dictionary
    username :str = Field(None,description="Username of student") 
    email: EmailStr = Field(description="User EMail")
    grade:  Optional[str] = Field(description=" grade of student")

class createStudentModel(studentModel):
    password : str = Field(default="pass1234",description="password of the student")

class updateStudentModel(BaseModel):
    username : Optional[str] = Field(None,description="Username of student") 
    grade:  Optional[str] = Field(description=" grade of student")
    password :  Optional[str] = Field(default="pass1234",description="password of the student")

