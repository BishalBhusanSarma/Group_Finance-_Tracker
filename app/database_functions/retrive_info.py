from sqlalchemy import select
from app.database_tables.user import User
from sqlalchemy.orm import Session

def get_user_by_id(user_id:int, db:Session):
    statement = select(User).where(User.id == user_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()

def get_by_username(db:Session , username:str):
    statement = select(User).where(User.username == username)
    result = db.execute(statement)
    return result.scalar_one_or_none()

def get_by_email(db:Session, email:str):
    statement = select(User).where(User.email == email)
    result = db.execute(statement)
    return result.scalar_one_or_none()


