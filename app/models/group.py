from pydantic import BaseModel

class CreateGroup(BaseModel):
    group_name:str
    group_password:str

class JoinGroup(BaseModel):
    group_id:int
    group_password:str