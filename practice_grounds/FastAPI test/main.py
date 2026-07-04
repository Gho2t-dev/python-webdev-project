'''
# ============================================================
# FastAPI Demo — a tiny "to-do list" API to learn the basics
# ============================================================
# To run this:
#   1. pip install fastapi uvicorn
#   2. uvicorn demo:app --reload
#   3. Open http://127.0.0.1:8000/docs in your browser
#      (FastAPI auto-generates an interactive test page for you!)
# ============================================================

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# "app" is the core FastAPI application object.
# Every route (URL) we define gets attached to this.
app = FastAPI(title="My To-Do Demo API")


# ------------------------------------------------------------
# Pydantic model = defines the "shape" of data we expect.
# FastAPI uses this to automatically validate incoming JSON
# and to generate documentation.
# ------------------------------------------------------------
class Todo(BaseModel):
    title: str                  # required field, must be text
    done: bool = False          # optional field, defaults to False


# In-memory "database" — just a Python dict.
# Data disappears when the server restarts (it's only for learning!).
todos: dict[int, Todo] = {}
next_id = 1


# ------------------------------------------------------------
# @app.get("/") means: "when someone visits this URL with GET,
# run the function below."
# ------------------------------------------------------------
@app.get("/")
def read_root():
    # Whatever we return here is automatically converted to JSON.
    return {"message": "Welcome to the To-Do API!"}


# GET /todos -> list every to-do item
@app.get("/todos")
def list_todos():
    return todos


# POST /todos -> create a new to-do item
# "todo: Todo" tells FastAPI to read the request body as JSON
# and validate it against our Todo model above.
@app.post("/todos")
def create_todo(todo: Todo):
    global next_id
    todos[next_id] = todo
    next_id += 1
    return {"id": next_id - 1, "todo": todo}


# GET /todos/{todo_id} -> get one specific to-do by its id
# "{todo_id}" in the path becomes a function parameter.
@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    if todo_id not in todos:
        # HTTPException lets us return a proper error response
        # (404 = "Not Found") instead of crashing.
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos[todo_id]


# PUT /todos/{todo_id} -> update an existing to-do
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = todo
    return {"id": todo_id, "todo": todo}


# DELETE /todos/{todo_id} -> remove a to-do
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    if todo_id not in todos:
        raise HTTPException(status_code=404, detail="Todo not found")
    del todos[todo_id]
    return {"message": f"Todo {todo_id} deleted"}

'''

# This is my first self written API, it is a Quotes API that chas a fixed set of quotes
# you are als able to add yout own quotes. 
# a quote consists of id, quote, author, year
# ID will be auto assigned

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title = 'Quote library')

class Quote(BaseModel):
    quote: str
    author: str = 'Unknown'
    year: int = 2026

test_quote = Quote(quote = 'learning is best done by doing', author = 'Me')
test_quote2 = Quote(quote = 'Get it working first, then make it work perfect', author = 'Me')


quotes: dict[int, Quote] = {1: test_quote, 2: test_quote2}
next_id = 3

@app.get('/')
def welcome_message():
    return {
        'Message': 'Welcome to the quotes library',
        'Built by': 'Fabian Harrab'
        }

@app.get('/quotes')
def get_all_quotes():
    return quotes

@app.post('/quotes')
def add_new(quote: Quote):
    global next_id
    quotes[next_id] = quote
    next_id += 1
    return {
        'id': next_id - 1,
        'quote': quote
    }

@app.get('/quotes/{quote_id}')
def get_quote(quote_id: int):
    if quote_id not in quotes:
        raise HTTPException (status_code= 404, detail= 'quote not found')
    return quotes[quote_id]

@app.put('/quotes/{quote_id}')
def update_quote(quote_id: int, quote: Quote):
    if quote_id not in quotes:
        raise HTTPException (status_code= 404, detail= 'Quote does not exist')
    quotes[quote_id] = quote
    return {
        'id': quote_id,
        'quote': quote
    }

@app.delete('/quotes/{quote_id}')
def delete_quote(quote_id: int):
    if quote_id not in quotes:
        raise HTTPException (status_code= 404, detail= 'Quote does not exist')
    quotes.pop(quote_id)
    return {
        'message': 'succesfully removed',
        'removed quote ID': quote_id
    }