from app.database.base import Base
from sqlalchemy import DateTime, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Membership(Base):
    __tablename__ = "membership"

    __table_args__ = (UniqueConstraint("group_id", "user_id"),)

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id:Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    user_id:Mapped[int] = mapped_column(ForeignKey("user_details.id"), nullable=False)
    is_admin:Mapped[bool] = mapped_column(Boolean, nullable= False, default=False)
    
    joined_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)