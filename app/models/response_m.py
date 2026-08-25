from pydantic import BaseModel, ConfigDict

class LoginResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    username:str
    email:str
    phone:str
class GroupResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id:int
    group_name:str
    admin_id:int

class JoinGroup(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    group_id:int
    msg:str = "Group Joined"

class CreateExpense(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    group_id:int
    total:float
    tags:str
    description:str