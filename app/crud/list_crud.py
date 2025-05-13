from ..models.list_model import ListModel
from ..schemas.list_schema import NewTodoList, UpdateTodoList, ResponseTodoList

from sqlalchemy.orm import Session


def get_todo_list(db: Session, todo_list_id):
    try:
        db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
        return db_item
    finally:
        db.close()


def post_todo_list(db: Session, new_todo_list: NewTodoList):
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


def put_todo_list(db: Session, todo_list_id: int, updated_data: UpdateTodoList):
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


def delete_todo_list(db: Session, todo_list_id: int):
    try:
        db_item = db.query(ListModel).filter(ListModel.id == todo_list_id).first()
        db.delete(db_item)

        db.commit()

        return {}
    finally:
        db.close()
