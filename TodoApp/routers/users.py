from fastapi import APIRouter, HTTPException, status
from pydantic import Field, BaseModel

from models import Users
from .auth import get_current_user, user_dependency
from utils import bcrypt_context, db_dependency

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)

@router.get("/info", status_code=status.HTTP_200_OK)
async def simple(user: user_dependency, db: db_dependency):
    return db.query(Users).filter(Users.id == user.get("id")).first()

@router.post("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_verification: UserVerification):
    user_model: Users = db.query(Users).filter(Users.id == user.get("id")).first()
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Password didn't match"
        )
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.commit()