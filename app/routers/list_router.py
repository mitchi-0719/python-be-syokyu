from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud import list_crud
from app.schemas.list_schema import NewTodoList, UpdateTodoList
from app.dependencies import get_db


router = APIRouter(
    prefix="/lists",
    tags=["Todoリスト"],
)


@router.get("/")
def get_todo_lists(db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    return list_crud.get_todo_lists(db, page, per_page)


@router.get("/{todo_list_id}")
def get_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    lst = list_crud.get_todo_list(db, todo_list_id)
    if lst is None:
        raise HTTPException(status_code=404, detail="todo list not found")
    return lst


@router.post("/")
def post_todo_list(todo_list: NewTodoList, db: Session = Depends(get_db)):
    if not todo_list.title:
        raise HTTPException(status_code=404, detail="list not found")
    return list_crud.create_todo_list(db, todo_list)


@router.put("/{todo_list_id}")
def put_todo_list(
    todo_list_id: int, todo_list: UpdateTodoList, db: Session = Depends(get_db)
):
    if get_todo_list(todo_list_id, db) is None:
        raise HTTPException(status_code=404, detail="todo list not found")

    return list_crud.update_todo_list(db, todo_list_id, todo_list)


@router.delete("/{todo_list_id}")
def delete_todo_list(todo_list_id: int, db: Session = Depends(get_db)):
    if get_todo_list(todo_list_id, db) is None:
        raise HTTPException(status_code=404, detail="todo list not found")
    return list_crud.delete_todo_list(db, todo_list_id)
