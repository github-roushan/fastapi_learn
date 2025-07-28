from fastapi import APIRouter, Path, status, HTTPException
from pydantic import BaseModel, Field
from models import Todos
from utils import db_dependency, is_admin
from .auth import user_dependency

router = APIRouter(
    prefix = "/admin",
    tags = ["Admin"]
)


@router.get("/todo", status_code=status.HTTP_200_OK)
@is_admin
async def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
@is_admin
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    query_result = db.query(Todos).filter(Todos.id == todo_id).delete()
    if query_result == 0:
        raise HTTPException(
            status_code=404,
            detail="Todo Not Found"
        )
    db.commit()