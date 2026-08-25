from sqlalchemy import select, func
from app.database_tables.groups import Group
from app.database_tables.members import Membership
from app.database_tables.group_expense import GroupExpense

from sqlalchemy.orm import Session

def get_group_details(group_id:int, db:Session):
    statement = select(Group).where(Group.id == group_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()

def get_members_details(member:int, group_id:int, db:Session):
    statement = select(Membership).where(Membership.user_id == member, Membership.group_id == group_id)
    result = db.execute(statement)
    return result.scalar_one_or_none()

def get_group_expense(group_id:int, db:Session):

    statement = select(GroupExpense).where(GroupExpense.group_id == group_id)
    result = db.execute(statement)
    return result.scalars().all()



def get_total_expenses_by_user(group_id: int, db: Session):
    statement = (
        select(
            GroupExpense.member_id,
            func.sum(GroupExpense.total),
        )
        .where(GroupExpense.group_id == group_id)
        .group_by(GroupExpense.member_id)
    )

    result = db.execute(statement).all()

    return [
        {
            "user_id": user_id,
            "total_expense": total,
        }
        for user_id, total in result
    ]


def get_total_group_expense(group_id: int, db: Session):
    statement = select(func.sum(GroupExpense.total)).where(
        GroupExpense.group_id == group_id
    )

    total = db.execute(statement).scalar() or 0
    group_details = get_group_details(group_id,db)
    return {
        "group_id":group_id,
        "group_name": group_details.group_name,
        "total_expense": total,
    }