from typing import Annotated
from fastapi import Depends
from requests import Session
from database import SessionLocal
from passlib.context import CryptContext

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

## password hashing utility
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')