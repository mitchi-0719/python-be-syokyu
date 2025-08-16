from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.item_schema import NewTodoItem, UpdateTodoItem
from app.crud import item_crud
from app.dependencies import get_db


router = APIRouter(
    prefix="/lists/{todo_list_id}/items",
    tags=["TODOリスト"],
)


@router.get("/{todo_item_id}")
def get_todo_item(todo_list_id, todo_item_id, db: Session = Depends(get_db)):
    return item_crud.get_todo_item(db, todo_list_id, todo_item_id)


@router.post("/")
def post_todo_item(
    todo_list_id, new_todo_item: NewTodoItem, db: Session = Depends(get_db)
):
    return item_crud.post_todo_item(db, todo_list_id, new_todo_item)


@router.put("/{todo_item_id}")
def put_todo_item(
    todo_list_id,
    todo_item_id,
    update_todo_item: UpdateTodoItem,
    db: Session = Depends(get_db),
):
    return item_crud.put_todo_item(db, todo_list_id, todo_item_id, update_todo_item)


@router.delete("/{todo_item_id}")
def delete_todo_item(todo_list_id, todo_item_id, db: Session = Depends(get_db)):
    return item_crud.delete_todo_item(db, todo_list_id, todo_item_id)
