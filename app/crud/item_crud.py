from app.models.item_model import ItemModel
from app.schemas.item_schema import NewTodoItem, UpdateTodoItem

from app.const import TodoItemStatusCode
from sqlalchemy.orm import Session


def get_todo_items(db: Session, page, per_page):
    try:
        offset = (page - 1) * per_page
        db_item = db.query(ItemModel).offset(offset).limit(per_page).all()
        return db_item
    finally:
        db.close()


def get_todo_item(db: Session, todo_list_id, todo_item_id):
    try:
        db_item = (
            db.query(ItemModel)
            .filter(
                ItemModel.id == todo_item_id, ItemModel.todo_list_id == todo_list_id
            )
            .first()
        )

        return db_item
    finally:
        db.close()


def post_todo_item(db: Session, todo_list_id, new_todo_item: NewTodoItem):
    try:
        db_item = ItemModel(
            todo_list_id=todo_list_id,
            title=new_todo_item.title,
            description=new_todo_item.description,
            status_code=TodoItemStatusCode.NOT_COMPLETED.value,
            due_at=new_todo_item.due_at,
        )

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    finally:
        db.close()


def put_todo_item(
    db: Session, todo_list_id, todo_item_id, update_todo_item: UpdateTodoItem
):
    try:
        db_item = (
            db.query(ItemModel)
            .filter(
                ItemModel.id == todo_item_id and ItemModel.todo_list_id == todo_list_id
            )
            .first()
        )
        db_item.title = update_todo_item.title
        db_item.description = update_todo_item.description
        db_item.due_at = update_todo_item.due_at
        db_item.status_code = (
            TodoItemStatusCode.COMPLETED.value
            if update_todo_item.complete
            else TodoItemStatusCode.NOT_COMPLETED.value
        )

        db.commit()
        db.refresh(db_item)

        return db_item
    finally:
        db.close()


def delete_todo_item(db: Session, todo_list_id, todo_item_id):
    try:
        db_item = (
            db.query(ItemModel)
            .filter(
                ItemModel.todo_list_id == todo_list_id and ItemModel.id == todo_item_id
            )
            .first()
        )
        db.delete(db_item)
        db.commit()
        return {}
    finally:
        db.close()
