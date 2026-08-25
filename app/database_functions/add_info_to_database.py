from sqlalchemy.orm import Session
from app.database_tables.user import User
from app.database_tables.groups import Group
from app.database_tables.members import Membership
from app.database_tables.group_expense import GroupExpense

def create_user(db:Session, user:User):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_group(db:Session, group:Group):
    db.add(group)
    db.commit()
    db.refresh(group)
    return group

def create_membership(db:Session, membership:Membership):
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership

def create_group_expense(db:Session, group_expense:GroupExpense):
    db.add(group_expense)
    db.commit()
    db.refresh(group_expense)
    return group_expense