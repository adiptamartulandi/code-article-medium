from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="My Todo API",
    description="A simple todo list API built with FastAPI",
    version="1.0"
)


# ============================================
# DATA MODELS (Pydantic Schemas)
# ============================================

class TodoCreate(BaseModel):
    """Schema for creating a new todo.
    This defines what data the client must send."""
    title: str
    description: Optional[str] = None  # Optional field


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo.
    All fields are optional so the client can update only what they want."""
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None


class TodoResponse(BaseModel):
    """Schema for returning a todo to the client.
    This is what the API will respond with."""
    id: int
    title: str
    description: Optional[str] = None
    done: bool = False


# ============================================
# IN-MEMORY DATABASE
# ============================================
# For learning purposes, we use a Python list to store todos.
# The data lives in RAM — it's temporary and will be lost when the server restarts.
# In production, you'd use a real database (PostgreSQL, MySQL, SQLite).

todos: List[TodoResponse] = [
    TodoResponse(id=1, title="Learn FastAPI", description="Complete the basics tutorial", done=False),
    TodoResponse(id=2, title="Build a project", description="Apply what I learned", done=False),
]
next_id = 3  # Auto-increment counter for assigning IDs to new todos


# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
def read_root():
    return {"Welcome to ToDo list app"}


@app.get("/todos", response_model=List[TodoResponse])
def get_all_todos():
    """
    Returns all todos.
    GET /todos
    """
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int):
    """
    Returns a specific todo by its ID.
    GET /todos/1, GET /todos/2, etc.
    """
    for todo in todos:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")


@app.post("/todos", response_model=TodoResponse, status_code=201)
def create_todo(todo: TodoCreate):
    """
    Creates a new todo.
    POST /todos with JSON body: {"title": "Buy milk", "description": "Go to the store"}
    """
    global next_id
    
    new_todo = TodoResponse(
        id=next_id,
        title=todo.title,
        description=todo.description,
        done=False  # New todos are always not done
    )
    todos.append(new_todo)
    next_id += 1
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_data: TodoUpdate):
    """
    Updates an existing todo.
    PUT /todos/1 with JSON body: {"title": "New title", "done": true}
    All fields are optional — only provided fields will be updated.
    """
    for todo in todos:
        if todo.id == todo_id:
            # Only update fields that were actually provided
            if todo_data.title is not None:
                todo.title = todo_data.title
            if todo_data.description is not None:
                todo.description = todo_data.description
            if todo_data.done is not None:
                todo.done = todo_data.done
            return todo
    raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int):
    """
    Deletes a todo.
    DELETE /todos/1
    Returns 204 No Content on success.
    """
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return  # 204 status means no response body
    raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found")
