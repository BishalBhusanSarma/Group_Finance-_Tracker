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
from app.database_functions.retrive_info_group import get_group_expense, get_members_details, get_total_expenses_by_user, get_total_group_expense

expense_router = APIRouter(prefix="/Expense", tags=["Track Expense"])

@expense_router.get("/check_group_expense")
def check_group_expense(group_id:int, user: str = Depends(validate_access_token), db: Session = Depends(get_db)):
    current_user = int(user)
    if not get_members_details(current_user,group_id ,db):
        raise HTTPException(status_code=403, detail="not in the group")
    
    return get_group_expense(group_id, db)

@expense_router.get("/check_group_expense_by_user")
def check_group_expense_by_user(group_id:int, user: str = Depends(validate_access_token), db: Session = Depends(get_db)):
    current_user = int(user)
    if not get_members_details(current_user,group_id ,db):
        raise HTTPException(status_code=403, detail="not in the group")
    
    return get_total_expenses_by_user(group_id, db)

@expense_router.get("/check_total_group_expense")
def check_total_group_expense(group_id:int, user: str = Depends(validate_access_token), db: Session = Depends(get_db)):
    current_user = int(user)
    if not get_members_details(current_user,group_id ,db):
        raise HTTPException(status_code=403, detail="not in the group")
    
    return get_total_group_expense(group_id, db)

