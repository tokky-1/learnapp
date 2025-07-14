from pydantic import BaseModel,Field

class Token(BaseModel):
    access_token: str 
    token_type : str

class studentauthmodel(BaseModel):
    username:str = Field ( description="usernamr of student")
    password: str = Field( description="password used at acct creation")