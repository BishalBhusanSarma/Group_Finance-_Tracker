from app.database.base import Base
from sqlalchemy import Text, String, Float, DateTime, ForeignKey, Identity
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
class Group(Base):
    __tablename__ = "groups"

    id:Mapped[int] = mapped_column(Identity(start=50000),primary_key=True)
    group_name:Mapped[str] = mapped_column(String(255), nullable=False)
    admin_id:Mapped[int] = mapped_column(ForeignKey("user_details.id"), nullable=False)
    hashed_password:Mapped[str] = mapped_column(Text, nullable=False)
    total:Mapped[float] = mapped_column(Float, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now,onupdate=datetime.now) 