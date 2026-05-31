from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# GET request — used to retrieve data (like fetching a webpage)
@app.get("/hello")
def hello_get():
    return {"message": "This is a GET request — used to read data"}


# POST request — used to create new data (like submitting a form)
@app.post("/hello")
def hello_post():
    return {"message": "This is a POST request — used to create data"}


# PUT request — used to replace existing data (like updating your profile)
@app.put("/hello")
def hello_put():
    return {"message": "This is a PUT request — used to replace data"}


# DELETE request — used to delete data (like removing an account)
@app.delete("/hello")
def hello_delete():
    return {"message": "This is a DELETE request — used to delete data"}

# Dummy data
users = [
    {"id": 1, "name": "Alice", "age": 25, "city": "Jakarta"},
    {"id": 2, "name": "Bob", "age": 30, "city": "Bandung"},
    {"id": 3, "name": "Charlie", "age": 22, "city": "Jakarta"},
    {"id": 4, "name": "Diana", "age": 28, "city": "Surabaya"},
]

@app.get("/users/{user_id}/items/{item_id}")
def get_user_item(user_id: int, item_id: int):
    return {
        "user_id": user_id,
        "item_id": item_id,
        "message": f"User {user_id} is viewing item {item_id}"
    }

@app.get("/users")
def get_users(age: int = None, city: str = None):
    """
    Returns users, optionally filtered by age and/or city.
    Both parameters are optional (they have default values of None).
    """
    result = users
    
    if age is not None:
        result = [u for u in result if u["age"] == age]
    
    if city is not None:
        result = [u for u in result if u["city"].lower() == city.lower()]
    
    return {
        "users": result,
        "count": len(result),
        "filters_applied": {
            "age": age,
            "city": city
        }
    }

# Step 1: Define a Pydantic model — this describes what data we expect
class User(BaseModel):
    name: str           # Required — must be a string
    age: int            # Required — must be an integer
    email: str          # Required — must be a string
    is_active: bool = True  # Optional — defaults to True if not provided


# Step 2: Use the model in your endpoint
@app.post("/users")
def create_user(user: User):
    return {
        "message": f"User {user.name} created successfully!",
        "user_data": user
    }
