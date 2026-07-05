# This will be the API to communicate between frontend and the database.py file.

from fastapi import FastAPI, Depends
from pydantic import BaseModel
import sqlite3
import database
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    con = sqlite3.connect('learning_tracker_lite.db')
    database.init_db(con)
    con.close()
    yield

app = FastAPI(title = 'logged lite API', lifespan = lifespan)

# get_db() for extablishing a db connection and 'killing' it again once the request is done
def get_db():
    con = sqlite3.connect('learning_tracker_lite.db') # Get connection
    yield con # Pass connection to whatever calls it and wait
    con.close() # close connection once finished

@app.get('/')
def display_all_entries(con = Depends(get_db)):
    all_entries = database.show_all(con)
    structured_entries = {}
    for entry in all_entries:
        entries = {
            'subject': entry[1],
            'key_learnings': entry[2],
            'notes': entry[3],
            'time_spent': entry[4],
            'difficulty': entry[5],
            'datetime': entry[6]
        }
        structured_entries[entry[0]] = entries
    return structured_entries