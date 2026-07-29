# Quote Library API
#
# A small FastAPI backend for storing and serving quotes.
# Data lives in memory (a plain Python dict) so it resets whenever the
# server restarts -- that's fine for a demo/learning project.
#
# Run it with:
#   uvicorn main:app --reload
#
# Then open the docs at http://127.0.0.1:8000/docs to try it out.

import random

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Quote Library")

# Browsers block JS from calling an API on a different origin unless the
# API explicitly allows it -- that's what CORS middleware is for.
# allow_origins=["*"] is fine here because this is a local learning
# project with no auth/cookies involved. In a real product you'd list
# your actual frontend domain(s) instead of "*".
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Quote(BaseModel):
    """Shape of a quote sent to us by the client (no id yet -- we assign that)."""
    quote: str = Field(min_length=1, description="The quote text itself")
    author: str = "Unknown"
    year: int = 2026


class QuoteOut(Quote):
    """Shape of a quote we send back -- same as Quote, plus its id."""
    id: int


# In-memory "database". Restarting the server wipes this back to the
# two seed quotes below.
quotes: dict[int, Quote] = {
    1: Quote(quote="Learning is best done by doing", author="Me"),
    2: Quote(quote="Get it working first, then make it work perfect", author="Me"),
}
next_id = 3


def as_out(quote_id: int, quote: Quote) -> QuoteOut:
    """Helper so every response includes the id alongside the quote fields."""
    return QuoteOut(id=quote_id, **quote.model_dump())


@app.get("/")
def welcome_message():
    return {
        "Message": "Welcome to the quotes library",
        "Built_by": "Fabian Harrab",
    }


@app.get("/quotes", response_model=list[QuoteOut])
def get_all_quotes():
    """Return every quote as a list (easier for the frontend to loop over than a dict)."""
    return [as_out(quote_id, quote) for quote_id, quote in quotes.items()]


@app.get("/quotes/random", response_model=QuoteOut)
def get_random_quote():
    # IMPORTANT: this route must be declared before /quotes/{quote_id},
    # otherwise FastAPI would try to match "random" as an int id and 422.
    if not quotes:
        raise HTTPException(status_code=404, detail="No quotes yet")
    quote_id = random.choice(list(quotes.keys()))
    return as_out(quote_id, quotes[quote_id])


@app.get("/quotes/{quote_id}", response_model=QuoteOut)
def get_quote(quote_id: int):
    if quote_id not in quotes:
        raise HTTPException(status_code=404, detail="Quote not found")
    return as_out(quote_id, quotes[quote_id])


@app.post("/quotes", response_model=QuoteOut, status_code=201)
def add_quote(quote: Quote):
    global next_id
    new_id = next_id
    quotes[new_id] = quote
    next_id += 1
    return as_out(new_id, quote)


@app.put("/quotes/{quote_id}", response_model=QuoteOut)
def update_quote(quote_id: int, quote: Quote):
    if quote_id not in quotes:
        raise HTTPException(status_code=404, detail="Quote not found")
    quotes[quote_id] = quote
    return as_out(quote_id, quote)


@app.delete("/quotes/{quote_id}")
def delete_quote(quote_id: int):
    if quote_id not in quotes:
        raise HTTPException(status_code=404, detail="Quote not found")
    quotes.pop(quote_id)
    return {"message": "Successfully removed", "removed_quote_id": quote_id}
