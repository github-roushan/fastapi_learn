from typing import Annotated
from fastapi import FastAPI, Depends, Path, status, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from models import Todos, Base
from database import engine, SessionLocal

app = FastAPI()

Base.metadata.create_all(bind = engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
class TodoRequest(BaseModel):
    title: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

    class Config:
        json_schema_extra = {
            "example": {
                "title": "A sample todo",
                "description": "What to do",
                "priority": 5,
                "complete": False
            }
        }

@app.get("/")
async def get_all_todos(db: db_dependency):
    return db.query(Todos).all()

@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo With id: {todo_id} not found")

@app.post("/create_todo", status_code=status.HTTP_200_OK)
async def create_todo(todo: TodoRequest, db: db_dependency):
    todo = Todos(**todo.model_dump())
    db.add(todo)
    db.commit()
    return {"message": "Added a todo"}