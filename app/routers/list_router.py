
from fastapi import APIRouter

router = APIRouter(
    prefix="/lists",
    tags=["TODOリスト"],
)

@app.get("/lists/{todo_list_id}", tags=["Todoリスト"])
def 

@app.post("/lists", tags=["Todoリスト"])
@app.put("/lists/{todo_list_id}", tags=["Todoリスト"])
@app.delete("/lists/{todo_list_id}", tags=["Todoリスト"])