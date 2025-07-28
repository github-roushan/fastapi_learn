from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from models import Users
from utils import db_dependency, bcrypt_context
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from models import RoleEnum
from settings import BASE_DIR

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

load_dotenv(dotenv_path=f"{BASE_DIR}/.env")
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv("ALGORITHM")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token/generate")

class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: RoleEnum

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

class Token(BaseModel):
    access_token: str
    token_type: str

def authenticate_user(username: str, password: str, db):
    if ( user := db.query(Users).filter(Users.username == username).first()):
        if bcrypt_context.verify(password, user.hashed_password):
            return True,user
    return False, None

def create_access_token(username: str, user_id: int, role: str, time_to_live: timedelta):
    encode = {"sub": username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + time_to_live
    encode['exp'] = expires
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could Not Validate User"
            )
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Could Not Validate User"
            )
    
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.post("/create", status_code=status.HTTP_201_CREATED)
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

    return {"detail": "User Successfully created"}

@router.post("/token/generate", status_code=status.HTTP_200_OK, response_model=Token)
async def generate_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    is_authenticated, user = authenticate_user(form_data.username, form_data.password, db)
    if is_authenticated:
        token = create_access_token(user.username, user.id, user.role.value, timedelta(minutes=30))
        return {"access_token": token, "token_type":"Bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Username or password"
    )

@router.get("/list/users", status_code = status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    return db.query(Users).all()