# This will be the API to communicate between frontend and the database.py file.

from fastapi import FastAPI, Depends, HTTPException , Response, status
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

# Pydantic model for new entry
class NewEntry(BaseModel):
	subject: str
	key_learnings: str
	notes: str = 'no notes'
	time_spent: float
	difficulty: int

# get_db() for extablishing a db connection and 'killing' it again once the request is done
def get_db():
    con = sqlite3.connect('learning_tracker_lite.db') # Get connection
    yield con # Pass connection to whatever calls it and wait
    con.close() # close connection once finished

# API root welcome message
@app.get('/')
def root():
    return {'message': 'Welcome to the API of the logged lite app!'}

# return ALL log entries nicely structured as a dictionary
@app.get('/logs')
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

# return a single entry by ID
@app.get('/logs/{entry_id}')
def display_entry(entry_id: int, con = Depends(get_db)): # defined parameters always have to be after undefined ones.
    
    # Check if ID is in database and raise exception if not
    result = database.check_id(con, entry_id)
    if result == None:
        raise HTTPException (status_code= 404, detail= 'This entry does not exist, please double check the id')
    
    entry = database.show_entry(con, entry_id)
    for i in entry:
        structured_entry = {
            'id': i[0],
            'subject': i[1],
            'key_learnings': i[2],
            'notes': i[3],
            'time_spent': i[4],
            'difficulty': i[5],
            'datetime': i[6]
        }
    return structured_entry

# create a new entry
@app.post('/logs')
def create_entry(new_entry: NewEntry, response: Response, con = Depends(get_db)):

    # transform the new entry to a tupple
    tuppled_entry = (new_entry.subject, new_entry.key_learnings, new_entry.notes, new_entry.time_spent, new_entry.difficulty)
    
    # IMPORTANT new entry is a object so it is called via .subject etc.
    
    database.add_entry(con, tuppled_entry)
    response.status_code = status.HTTP_201_CREATED 
    # Wäre auch einfacher: 
    # FastAPI also lets you set status_code=201 directly in the route decorator (@app.post('/logs', status_code=201))
    return {'added successfully': new_entry}

# Delete existing entry
@app.delete('/logs/{entry_id}')
def delete_entry(entry_id: int, con = Depends(get_db)):
    # Check if ID is in database and raise exception if not
    result = database.check_id(con, entry_id)
    if result == None:
        raise HTTPException (status_code= 404, detail= 'This entry does not exist, please double check the id')
    
    # Delete entry
    database.delete_entry(con, entry_id)
    return {'message': f'entry with id {entry_id}, deleted successfuly'}

# Update COMPLETE existing entry
@app.put('/logs/{entry_id}')
def update_full_entry(entry_id: int, new_entry: NewEntry, con = Depends(get_db)):
    # Check if ID is in database and raise exception if not
    result = database.check_id(con, entry_id)
    if result == None:
        raise HTTPException (status_code= 404, detail= 'This entry does not exist, please double check the id')
    
    # transform the new entry to a tupple
    tuppled_entry = (new_entry.subject, new_entry.key_learnings, new_entry.notes, new_entry.time_spent, new_entry.difficulty)
    
    # IMPORTANT new entry is a object so it is called via .subject etc.
    
    database.edit_full_entry(con, entry_id, tuppled_entry)
    return {'added successfully': new_entry}