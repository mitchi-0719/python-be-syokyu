import os
from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.const import TodoItemStatusCode

from .models.item_model import ItemModel
from .models.list_model import ListModel

from fastapi import Depends
from .dependencies import get_db
from sqlalchemy.orm import Session

DEBUG = os.environ.get("DEBUG", "") == "true"

app = FastAPI(
    title="Python Backend Stations",
    debug=DEBUG,
)

if DEBUG:
    from debug_toolbar.middleware import DebugToolbarMiddleware

    # panelsに追加で表示するパネルを指定できる
    app.add_middleware(
        DebugToolbarMiddleware,
        panels=["app.database.SQLAlchemyPanel"],
    )


class NewTodoItem(BaseModel):
    """TODO項目新規作成時のスキーマ."""

    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo Item Description", min_length=1, max_length=200
    )
    due_at: datetime | None = Field(default=None, title="Todo Item Due")


class UpdateTodoItem(BaseModel):
    """TODO項目更新時のスキーマ."""

    title: str | None = Field(
        default=None, title="Todo Item Title", min_length=1, max_length=100
    )
    description: str | None = Field(
        default=None, title="Todo Item Description", min_length=1, max_length=200
    )
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    complete: bool | None = Field(
        default=None, title="Set Todo Item status as completed"
    )


class ResponseTodoItem(BaseModel):
    id: int
    todo_list_id: int
    title: str = Field(title="Todo Item Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo Item Description", min_length=1, max_length=200
    )
    status_code: TodoItemStatusCode = Field(title="Todo Status Code")
    due_at: datetime | None = Field(default=None, title="Todo Item Due")
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


class NewTodoList(BaseModel):
    """TODOリスト新規作成時のスキーマ."""

    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo List Description", min_length=1, max_length=200
    )


class UpdateTodoList(BaseModel):
    """TODOリスト更新時のスキーマ."""

    title: str | None = Field(
        default=None, title="Todo List Title", min_length=1, max_length=100
    )
    description: str | None = Field(
        default=None, title="Todo List Description", min_length=1, max_length=200
    )


class ResponseTodoList(BaseModel):
    """TODOリストのレスポンススキーマ."""

    id: int
    title: str = Field(title="Todo List Title", min_length=1, max_length=100)
    description: str | None = Field(
        default=None, title="Todo List Description", min_length=1, max_length=200
    )
    created_at: datetime = Field(title="datetime that the item was created")
    updated_at: datetime = Field(title="datetime that the item was updated")


@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def get_todo_list(todo_list_id):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
        return db_item
    finally:
        db.close()


@app.post("/lists", tags=["Todoリスト"])
def post_todo_list(new_todo_list: NewTodoList):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_item = ListModel(
            title=new_todo_list.title,
            description=new_todo_list.description,
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    finally:
        db.close()


@app.put("/lists/{todo_list_id}", tags=["Todoリスト"])
def put_todo_list(todo_list_id: int, updated_data: UpdateTodoList):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()

        if updated_data.title is not None:
            db_item.title = updated_data.title
        if updated_data.description is not None:
            db_item.description = updated_data.description

        db.commit()
        db.refresh(db_item)

        return db_item
    finally:
        db.close()


@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])
def delete_todo_list(todo_list_id: int):
    db_generator = get_db()
    db = next(db_generator)
    try:
        db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
        db.delete(db_item)

        db.commit()

        return {}
    finally:
        db.close()


@app.get("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todoリスト"])
def get_todo_item(todo_list_id, todo_item_id):
    db_generator = get_db()
    db = next(db_generator)
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


@app.post("/lists/{todo_list_id}/items", tags=["Todoリスト"])
def post_todo_item(todo_list_id, new_todo_item: NewTodoItem):
    db_generator = get_db()
    db = next(db_generator)
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


@app.put("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todoリスト"])
def put_todo_item(todo_list_id, todo_item_id, update_todo_item: UpdateTodoItem):
    db_generator = get_db()
    db = next(db_generator)
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


@app.delete("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todoリスト"])
def delete_todo_item(todo_list_id, todo_item_id):
    db_generator = get_db()
    db = next(db_generator)
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
