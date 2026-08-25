from pydantic import BaseModel

class Register(BaseModel):
    name:str
    username:str
    email:str
    phone:str
    password:str

class Login(BaseModel):
    details:str #username/email
    password:str