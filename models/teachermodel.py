from pydantic import BaseModel,Field,EmailStr
from typing import Optional

class teacherModel(BaseModel):
    username : str = Field(None,description="Username of teacher") 
    email: EmailStr = Field(description="User EMail")
    grade: Optional[str] = Field(description=" grade of teacher")

class createteacherModel(teacherModel):
    password : str = Field(default="pass1234",description="password of the teacher")


class updateTeacherModel(BaseModel):
    username : Optional[str] = Field(None,description="Username of teacher") 
    grade:  Optional[str] = Field(description=" grade of teacher")
    password :  Optional[str] = Field(default="pass1234",description="password of the teacher")


