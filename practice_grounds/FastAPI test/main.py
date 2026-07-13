# This is my first self written API, it is a Quotes API that chas a fixed set of quotes
# you are als able to add yout own quotes. 
# a quote consists of id, quote, author, year
# ID will be auto assigned

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title = 'Quote library')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"], # My frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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