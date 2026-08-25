from sqlalchemy import create_engine, Integer, String, text
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings


engine = create_engine(settings.DATABASE_URL, echo=settings.DEBUG)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# def check_db_connection():
#     try:
#         with engine.connect() as connection:
#             connection.execute(text("SELECT 1"))
#         print("Database connected successfully")
#     except Exception as error:
#         print(f"Database connection failed: {error}")

# check_db_connection()




