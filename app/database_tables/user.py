from app.database.base import Base
from sqlalchemy import Text, String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = "user_details"

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False)
    username:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    phone:Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email:Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    total:Mapped[float] = mapped_column(Float, default=0)
    hashed_password:Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)