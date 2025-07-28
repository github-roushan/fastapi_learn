from fastapi import APIRouter, Path, status, HTTPException
from pydantic import BaseModel, Field
from models import Todos
from utils import db_dependency

router = APIRouter()

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

@router.get("/")
async def get_all_todos(db: db_dependency):
    return db.query(Todos).all()

@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail=f"Todo With id: {todo_id} not found")

@router.post("/create_todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_model: TodoRequest, db: db_dependency):
    todo_model = Todos(**todo_model.model_dump())
    db.add(todo_model)
    db.commit()
    return {"message": "Added a todo"}

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail=f"No Such Todo with id: {todo_id}")
    
    for key, value in todo_request.dict().items():
        setattr(todo_model, key, value)

    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    query_result = db.query(Todos).filter(Todos.id == todo_id).delete()
    if query_result == 0:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )
    db.commit()