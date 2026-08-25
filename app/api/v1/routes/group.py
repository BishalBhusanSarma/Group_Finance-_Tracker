from fastapi import APIRouter, Depends, HTTPException
from app.models.userdetails import Register
from app.database_functions.add_info_to_database import create_group as cg, create_membership, create_group_expense
from app.database_tables.groups import Group
from app.database_tables.members import Membership
from app.database_tables.group_expense import GroupExpense
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.hashing.pwd_hashing import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from app.database_functions.retrive_info import get_by_username, get_user_by_id
from app.hashing.pwd_hashing import verify_password
from app.jwt.token import create_access_token, create_refresh_token, validate_access_token
from app.models.response_m import GroupResponse, JoinGroup, CreateExpense
from app.models.group import CreateGroup, JoinGroup as JG
from app.database_functions.retrive_info_group import get_group_details, get_members_details

group_router = APIRouter(prefix="/group", tags=["Create Group"])

@group_router.post("/create_group", response_model=GroupResponse)
def create_group(group_details:CreateGroup, admin: str = Depends(validate_access_token), db: Session = Depends(get_db)):
    group_hash_password = hash_password(group_details.group_password)

    group = Group(group_name = group_details.group_name, admin_id = int(admin), hashed_password = group_hash_password)

    new_group = cg(db, group)
    member = Membership(group_id = new_group.id, user_id = admin, is_admin = True)
    create_membership(db, member)
    
    return new_group

@group_router.post("/join_group", response_model=JoinGroup)
def join_group(group_details:JG, user: str = Depends(validate_access_token), db: Session = Depends(get_db)):
    password = group_details.group_password
    group_info = get_group_details(group_details.group_id, db)
    current_user = int(user)
    hashed_password = group_info.hashed_password
    

    if not verify_password(password, hashed_password):
        raise HTTPException(status_code=401, detail="Password didnt match")

    if get_members_details(current_user,group_details.group_id ,db):
        raise HTTPException(status_code=301, detail="User already joined")
    

    member = Membership(group_id = group_details.group_id, user_id = current_user)
    new_member = create_membership(db, member)
    return new_member

@group_router.post("/expense")
def create_expense(expense_details:CreateExpense, user: str = Depends(validate_access_token), db: Session = Depends(get_db)):

    current_user = int(user)
    if get_members_details(current_user,expense_details.group_id ,db):
        
        member_group_expense = GroupExpense(group_id = expense_details.group_id, member_id = current_user, total = expense_details.total, tags = expense_details.tags, description = expense_details.description)

        return create_group_expense(db, member_group_expense)
    else:
        raise HTTPException(status_code=403, detail="User not in group")


