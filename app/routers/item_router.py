from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.item_schema import NewTodoItem, UpdateTodoItem
from app.crud import item_crud, list_crud
from app.dependencies import get_db


router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["TODOリスト"],
)


@router.get("/")
def get_todo_items(db: Session = Depends(get_db), page: int = 1, per_page: int = 10):
    return item_crud.get_todo_items(db, page, per_page)


@router.get("/{todo_item_id}")
def get_todo_item(todo_list_id, todo_item_id, db: Session = Depends(get_db)):
    lst = item_crud.get_todo_item(db, todo_list_id, todo_item_id)
    if lst is None:
        raise HTTPException(status_code=404, detail="todo list not found")
    return lst


@router.post("/")
def post_todo_item(
    todo_list_id, new_todo_item: NewTodoItem, db: Session = Depends(get_db)
):
    lst = list_crud.get_todo_list(db, todo_list_id)
    if not lst:
        raise HTTPException(status_code=404, detail="Todo list not found")

    if not new_todo_item.title:
        raise HTTPException(status_code=404, detail="list not found")
    return item_crud.post_todo_item(db, todo_list_id, new_todo_item)


@router.put("/{todo_item_id}")
def put_todo_item(
    todo_list_id,
    todo_item_id,
    update_todo_item: UpdateTodoItem,
    db: Session = Depends(get_db),
):
    if get_todo_item(todo_list_id, todo_item_id, db) is None:
        raise HTTPException(status_code=404, detail="todo list not found")
    return item_crud.put_todo_item(db, todo_list_id, todo_item_id, update_todo_item)


@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id, todo_item_id, db: Session = Depends(get_db)):
    if get_todo_item(todo_list_id, todo_item_id, db) is None:
        raise HTTPException(status_code=404, detail="todo list not found")
    return item_crud.delete_todo_item(db, todo_list_id, todo_item_id)
