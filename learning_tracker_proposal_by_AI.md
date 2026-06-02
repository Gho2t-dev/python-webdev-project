# Project Proposal: Learning Tracker
### A Personal Web App to Log, Categorize, and Reflect on What You Learn

---

## What You're Building

A full-stack web application where you can log learning sessions — recording what you studied,
how long you spent on it, what context it was for (school, work, personal), and what kind of
subject it was (programming, language, math, etc.). Over time, the app builds a history you
can filter, search, and get simple stats from.

This is a project you will actually use, and it covers every layer of modern web development:
data storage, server logic, HTTP communication, and a browser interface.

---

## The Data Model

This is the most important design decision — get this right first and everything else follows.

### Table: `learning_logs`

| Column             | Type      | Required | Notes                                              |
|--------------------|-----------|----------|----------------------------------------------------|
| `id`               | INTEGER   | yes      | Primary key, auto-incremented                      |
| `title`            | TEXT      | yes      | Short label, e.g. "FastAPI routing"                |
| `notes`            | TEXT      | no       | Optional longer description of what you learned    |
| `subject`          | TEXT      | yes      | e.g. "Python", "French", "Calculus"                |
| `context`          | TEXT      | yes      | One of: `private`, `school`, `work`                |
| `category`         | TEXT      | yes      | See valid values below                             |
| `duration_minutes` | INTEGER   | yes      | How long the session was                           |
| `difficulty`       | INTEGER   | no       | Scale of 1–10 (1 = trivial, 10 = brutal)           |
| `usefulness`       | TEXT      | no       | One of: `low`, `medium`, `high`                    |
| `enjoyment`        | TEXT      | no       | One of: `😴`, `😐`, `🙂`, `🤩`                    |
| `logged_at`        | TEXT      | yes      | Date of the session (ISO format: YYYY-MM-DD)       |
| `created_at`       | TEXT      | yes      | Timestamp of when the record was inserted          |

### Valid Category Values

| Value                | Description                               |
|----------------------|-------------------------------------------|
| `programming`        | General coding, software development      |
| `ai_ml`              | Artificial intelligence, machine learning |
| `language`           | Spoken/written languages                  |
| `math`               | Mathematics, statistics                   |
| `science`            | Physics, chemistry, biology, etc.         |
| `cars_engines`       | Vehicles, mechanics, engineering          |
| `history`            | History, social sciences                  |
| `art_design_music`   | Creative disciplines                      |
| `business_finance`   | Business, economics, personal finance     |
| `health_fitness`     | Sports, fitness, nutrition, wellbeing     |
| `philosophy_psych`   | Philosophy, psychology, mindset           |
| `writing_literature` | Writing craft, literature, reading        |
| `general_knowledge`  | Miscellaneous topics that don't fit above |
| `other`              | Anything else                             |

### A note on the optional ratings

`difficulty`, `usefulness`, and `enjoyment` are optional — you do not have to fill
them in every time. However, be aware: if only half your entries have a difficulty
rating, any average difficulty stat you calculate will only reflect those entries.
This is a trade-off between flexibility and data quality worth thinking about as you use it.

**Why SQLite?**
No installation, no server, no configuration. It is a single `.db` file on your disk.
Perfect for a single-user personal app. If you ever scale this or add users, migrating
to PostgreSQL is straightforward — the SQL you write now transfers almost verbatim.

**Why not separate tables for `subject`, `context`, `category`?**
You could normalize this into multiple tables (a common pattern), but for a first project
the extra complexity is not worth it. Simple TEXT columns with a defined set of valid values
is easier to understand, easier to query, and still clean.

**Why store emojis as TEXT?**
SQLite stores text as UTF-8, which fully supports emojis. Storing `🤩` directly is
perfectly valid and makes your data human-readable when you inspect the database.

---

## The Stack

### Backend
| Tool       | Role                                      | Why this choice                                          |
|------------|-------------------------------------------|----------------------------------------------------------|
| Python 3.x | Language                                  | What you already know                                    |
| FastAPI    | Web framework / API layer                 | Modern, fast, readable. Auto-generates interactive docs at `/docs` — great for testing your endpoints without a frontend |
| Uvicorn    | ASGI server (runs FastAPI)                | Required by FastAPI, one-line startup                    |
| Pydantic   | Data validation                           | Comes with FastAPI. Validates incoming data automatically |
| sqlite3    | Database driver                           | Built into Python — no install needed                    |

### Frontend
| Tool                    | Role                   | Why this choice                                          |
|-------------------------|------------------------|----------------------------------------------------------|
| HTML5                   | Structure              | Foundation — no shortcuts yet                            |
| CSS3 (Flexbox/Grid)     | Layout & styling       | Modern layout tools that are used everywhere             |
| JavaScript (Fetch API)  | Dynamic behaviour      | No framework — you will understand every line you write  |

**Why no React/Vue yet?**
Frameworks hide what is actually happening. You will learn far more by using vanilla
JavaScript first. Once you understand how `fetch()`, DOM manipulation, and event listeners
work, a framework like React will make complete sense. Jumping to React now would mean
copying patterns without understanding them.

---

## API Endpoints

These are the URLs your frontend will talk to:

| Method | Route                   | What it does                                  |
|--------|-------------------------|-----------------------------------------------|
| GET    | `/api/logs`             | Returns all log entries (supports filtering)  |
| POST   | `/api/logs`             | Creates a new log entry                        |
| GET    | `/api/logs/{id}`        | Returns a single log entry by ID              |
| PUT    | `/api/logs/{id}`        | Updates an existing log entry                 |
| DELETE | `/api/logs/{id}`        | Deletes a log entry                           |
| GET    | `/api/stats`            | Returns summary statistics (totals, breakdowns)|

The `/api/stats` endpoint is what makes this interesting beyond a basic CRUD app.
It can return things like: total hours logged this week, breakdown by category,
most studied subject, etc.

---

## Project Phases

---

### Phase 1 — Database Layer
**Goal:** A working Python module that handles all database operations. No web server yet.

**Tasks:**
1. Create `schema.py` — a script that creates the `app.db` file and defines the table.
   Run this once to set up the database.
2. Create `database.py` — all CRUD functions:
   - `add_log(title, subject, context, category, duration, date, notes=None, difficulty=None, usefulness=None, enjoyment=None)`
   - `get_all_logs(context=None, category=None, usefulness=None)` — with optional filters
   - `get_log_by_id(id)`
   - `update_log(id, **fields)`
   - `delete_log(id)`
   - `get_stats()` — aggregation queries including:
     - Total sessions and total hours logged
     - Average difficulty across rated entries
     - Breakdown of usefulness ratings
     - Breakdown of enjoyment ratings
     - Most logged category and subject
3. Test every function directly in the terminal before moving on.

**You have finished Phase 1 when:**
You can call your functions from the terminal and see data correctly saved to and
retrieved from `app.db`.

---

### Phase 2 — FastAPI Backend
**Goal:** Wrap your Phase 1 functions in an HTTP server.

**Tasks:**
1. Create `main.py` — initialize FastAPI and Uvicorn.
2. Define Pydantic models for request validation:
   - `LogCreate` — what the client sends when creating a log
   - `LogUpdate` — what the client sends when editing a log
3. Wire each API route to its corresponding `database.py` function.
4. Enable CORS middleware (allows your browser frontend to call the API).
5. Test all endpoints using FastAPI's built-in `/docs` interface — you get this for free.

**You have finished Phase 2 when:**
You can open `http://localhost:8000/docs` and successfully create, read, update,
and delete log entries through the browser interface — without any custom frontend.

---

### Phase 3 — Frontend UI
**Goal:** A browser interface to interact with your API.

**Tasks:**
1. `index.html` — the main layout:
   - A form to add a new log entry (all fields)
   - A filter bar (by context, category, date range)
   - A table to display log entries
   - A simple stats panel (total sessions, total hours, breakdown)
2. `style.css` — clean, readable layout using Flexbox/Grid.
3. `app.js` — the logic:
   - On page load: fetch all logs from `GET /api/logs`, render them into the table
   - On form submit: send a `POST` request to create a new log, refresh the table
   - On delete button: send a `DELETE` request, remove the row from the table
   - On filter change: re-fetch with query parameters, re-render the table
   - Stats panel: fetch from `GET /api/stats`, render the numbers

**You have finished Phase 3 when:**
The whole app works end-to-end in the browser — you can log a session, see it appear
in the table, filter by category, and see updated stats, all without touching the terminal.

---

## Folder Structure

```
learning_tracker/
├── app.db                  # SQLite database (auto-generated, do not edit manually)
├── schema.py               # Run once to create the database and table
├── database.py             # All database functions (CRUD + stats)
├── main.py                 # FastAPI app — routes and server config
├── .env                    # Configuration variables (database path, etc.)
└── static/
    ├── index.html          # The browser UI
    ├── style.css           # Styling
    └── app.js              # Frontend logic (fetch calls, DOM updates)
```

**Why `.env`?**
Even on a local project, it is good practice to keep configuration out of your code.
The database file path, for example, does not belong hardcoded in `database.py`.
This habit matters enormously in professional environments.

---

## What You Will Know After This Project

By the time this is complete, you will understand:

- How to design a relational data model from scratch
- How to write and organize SQL queries inside Python
- How a REST API works — methods, routes, request/response cycle
- How HTTP communication works between a browser and a server
- How to validate incoming data before it touches your database
- How JavaScript talks to a backend without reloading the page
- How to structure a multi-file project cleanly

These are the exact foundations expected in any junior web development role.

---

## Suggested First Step

Start with `schema.py`. Write the SQL to create the `learning_logs` table,
run it, and confirm the `app.db` file appears on disk. That is it —
Phase 1 begins from there.
