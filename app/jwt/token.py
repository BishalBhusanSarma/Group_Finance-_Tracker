from jose import jwt,JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from datetime import datetime, timedelta, timezone


password_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

ACCESS = "access"
REFRESH = "refresh"

def create_access_token(user_id:int):
    exp = datetime.now(timezone.utc)+ timedelta(minutes=settings.ACCESS_TOKEN_EXPIRY)
    payload = {"sub":str(user_id),"type":ACCESS, "exp": exp}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(user_id:int):
    exp = datetime.now(timezone.utc)+ timedelta(days=settings.REFRESH_TOKEN_EXPIRY)
    payload = {"sub": str(user_id), "type": REFRESH, "exp": exp}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def validate_access_token(token: str = Depends(password_bearer)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != ACCESS:
            raise JWTError("Not an access token")
        return payload["sub"]
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

def validate_refresh_token(token:str = Depends(password_bearer)):
    try:
        user_details =  jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        
        if user_details["type"] != REFRESH:
            raise HTTPException(status_code=404, detail="User not found")
        return user_details["sub"]
    except:
        raise HTTPException(status_code=404, detail="User not found")
