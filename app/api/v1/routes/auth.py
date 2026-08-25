from fastapi import APIRouter, Depends, HTTPException
from app.models.userdetails import Register
from app.database_functions.add_info_to_database import create_user
from app.database_tables.user import User
from sqlalchemy.orm import Session
from app.database.dependencies import get_db
from app.hashing.pwd_hashing import hash_password
from fastapi.security import OAuth2PasswordRequestForm
from app.database_functions.retrive_info import get_by_username, get_user_by_id
from app.hashing.pwd_hashing import verify_password
from app.jwt.token import create_access_token, create_refresh_token, validate_access_token
from app.models.response_m import LoginResponse

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@auth_router.post("/register")
def register(data:Register, db:Session = Depends(get_db)):
    new_hashed_password = hash_password(data.password)
    user = User(name = data.name, username = data.username, phone = data.phone, email = data.email, hashed_password = new_hashed_password)
    new_user = create_user(db,user) 
    return new_user

@auth_router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_by_username(db, data.username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Wrong Password")
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type": "bearer",
    }


#********.    To Test Secure Root.      ********

# @auth_router.get("/sec", response_model=LoginResponse)
# def secure_route(user: str = Depends(validate_access_token), db: Session = Depends(get_db)):
#     return get_user_by_id(int(user), db)
