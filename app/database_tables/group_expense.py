from app.database.base import Base
from sqlalchemy import Text, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class GroupExpense(Base):
    __tablename__ = "group_expense"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id:Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    member_id:Mapped[int] = mapped_column(ForeignKey("user_details.id"), nullable=False)
    total:Mapped[float] = mapped_column(Float, default=0, nullable=False)
    tags:Mapped[str] = mapped_column(String(30), nullable=False, default="others")
    description:Mapped[str] = mapped_column(String(255),nullable=False, default="others")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,onupdate=datetime.now)