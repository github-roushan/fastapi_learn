from typing import Annotated
from fastapi import Depends, HTTPException, status
from requests import Session
from database import SessionLocal
from passlib.context import CryptContext
from functools import wraps

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

## password hashing utility
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

## Decorator to check for admin role
def is_admin(func):
    @wraps(func)
    async def wrapper(user, db, *args, **kwargs):
        if user is None or user.get("role") != "admin":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail = "Not an Admin"
            )
        return await func(user, db, *args, **kwargs)
    return wrapper