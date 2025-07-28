from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from models import Users
from hashlib import md5
from utils import db_dependency, bcrypt_context


router = APIRouter()

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "email": "email@xyz.com",
                "first_name": "Alan",
                "last_name": "Turing",
                "password": "pass123",
                "role": "admin"
            }
        }

@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_req: CreateUserRequest, db: db_dependency):
    if (existingUserEmail := db.query(Users).filter(Users.email == create_user_req.email).first()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email Already Registered")
    if (existingUserName := db.query(Users).filter(Users.username == create_user_req.username).first()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username Already Exists")
    
    user_data = create_user_req.model_dump(exclude={"password"})
    user_data["hashed_password"] = bcrypt_context.hash(create_user_req.password)
    create_user_model = Users(**user_data)

    db.add(create_user_model)
    db.commit()

    return {"message": "User Successfully created"}