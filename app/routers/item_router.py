from fastapi import APIRouter

router = APIRouter(
prefix="/lists",
tags=["TODOリスト"],
)



@app.get("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todoリスト"])



@app.post("/lists/{todo_list_id}/items", tags=["Todoリスト"])


@app.put("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todoリスト"])



@app.delete("/lists/{todo_list_id}/items/{todo_item_id}", tags=["Todoリスト"])