from fastapi import FastAPI, APIRouter
from app.hashing.pwd_hashing import hash_password
from app.jwt.token import create_access_token
from app.api.v1.routes.auth import auth_router
from app.api.v1.routes.group import group_router
from app.api.v1.routes.expense_track import expense_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(group_router)
app.include_router(expense_router)