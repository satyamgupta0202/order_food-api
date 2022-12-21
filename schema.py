from pydantic import BaseModel
from typing import Optional

class UserModel(BaseModel):
    id:Optional[int]
    username:str
    email:str
    password:str
    is_staff:Optional[bool]
    is_active:Optional[bool]

    class Config:
        orm_mode = True
        schema_extra={
            'example':{
                "username":"satyam0202",
                "email":"satyam@gmail.com",
                "password":"satyam0202",
                "is_staff":False,
                "is_active":True
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str = '57f384fdbbc2f6909b7da3faa34127ba3bbf0f1da5a5c6e479dc0e4ef7584f29'


class LoginModel(BaseModel):
   username:str
   password:str
   
    
