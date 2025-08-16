from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud import list_crud
from app.schemas.list_schema import NewTodoList, UpdateTodoList
from app.dependencies import get_db

router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


@router.get("/")
def get_todo_lists(db: Session = Depends(get_db)):
    return list_crud.get_todo_lists(db)


@router.get("/{todo_list_id}")
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    return list_crud.get_todo_list(db, todo_list_id)


@router.post("/")
def post_todo_list(todo_list: NewTodoList, db: Session = Depends(get_db)):
    return list_crud.create_todo_list(db, todo_list)


@router.put("/{todo_list_id}")
def put_todo_list(
    todo_list_id: int, todo_list: UpdateTodoList, db: Session = Depends(get_db)
):
    return list_crud.update_todo_list(db, todo_list_id, todo_list)


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    return list_crud.delete_todo_list(db, todo_list_id)
