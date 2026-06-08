# Full-Stack Learning Journey — Python Web Development

A documented learning path from Python fundamentals to a fully self-built, full-stack web application. Every file in this repo is a step toward one goal: building a personal learning tracker app called: **Logged**  — a real tool I will actually use, built entirely from scratch.

---

## The Goal

Build a full-stack web application called **Logged** where I can log study sessions, track time spent per subject, rate difficulty and usefulness, and see statistics about my learning habits over time.

This is not a tutorial project. It is a real app with a real data model, a real REST API, and a real browser UI — built by learning each layer of the stack from the ground up.

## My Background

I am a 22 year old engineer / engineering student from Switzerland. I work in a power semiconductor production plant where i maintain semiconductor production equipment. I studied for 4 years to get the "EFZ" as Automation Technician. I am currently working on my Professional Bachelors Degree in Systems Engineering at ABBTS. 

---

## Repository Structure

```
python-webdev-project/
├── practice_grounds/               # Standalone scripts — learning exercises
│   ├── sql_basics.py               # SQLite fundamentals (connect, create, insert)
│   ├── SQLite_Practice.py          # Early SQLite experiments
│   ├── OOP_Example_Code.py         # First look at OOP by AI: classes, inheritance, polymorphism
│   └── Database Viewer v1.0.py     # First real and selfmade CLI app: CRUD on a SQLite database
│
├── learning_tracker/               # The main project (built phase by phase)
│   ├── schema.py                   # [Phase 1] Creates app.db and the learning_logs table
│   ├── database.py                 # [Phase 1] All CRUD + stats functions
│   ├── main.py                     # [Phase 2] FastAPI app — routes and server config
│   ├── .env                        # [Phase 2] Config (db path, etc.)
│   ├── app.db                      # SQLite database — auto-generated, do not edit
│   └── static/
│       ├── index.html              # [Phase 3] Browser UI layout
│       ├── style.css               # [Phase 3] Styling (Flexbox/Grid)
│       └── app.js                  # [Phase 3] Fetch calls and DOM logic
│
├── logged_proposal_by_AI.md            # Full project spec and design rationale
└── .gitignore
```

> The `learning_tracker/` directory is built incrementally — files appear as each phase is completed.

---

## Progress

### Foundations (ongoing)

| File | What I practiced |
|------|-----------------|
| [sql_basics.py](practice_grounds/sql_basics.py) | Connecting to SQLite, creating tables, inserting rows with parameterized queries, fetching with filters, committing and closing connections (by AI for learning) |
| [SQLite_Practice.py](practice_grounds/SQLite_Practice.py) | First contact with the sqlite3 module and cursor pattern by myself |
| [Database Viewer v1.0.py](<practice_grounds/Database Viewer v1.0.py>) | First complete CLI app: interactive loop, input validation, parameterized SQL inserts, persistent SQLite storage |
| [OOP_Example_Code.py](practice_grounds/OOP_Example_Code.py) | Classes, `__init__`, instance attributes, encapsulation, inheritance, `super()`, method overriding, polymorphism, list comprehensions — using an equipment maintenance system as a real-world model (by AI for learning)|


---

### Phase 1 — Database Layer (Planned)

**Goal:** A Python module that handles all database operations. No web server yet.

**Deliverables:**
- `schema.py` — creates `app.db` and defines the `learning_logs` table
- `database.py` — CRUD functions plus a `get_stats()` aggregation query

**Done when:** Every function can be called from the terminal and data is correctly saved to and retrieved from `app.db`.

---

### Phase 2 — FastAPI Backend (Planned)

**Goal:** Wrap the Phase 1 database functions in an HTTP API server.

**Deliverables:**
- `main.py` — FastAPI app with Uvicorn, Pydantic validation models, CORS middleware
- All six REST endpoints wired to `database.py`

**Done when:** `http://localhost:8000/docs` is open and all endpoints work end-to-end through FastAPI's built-in UI — no custom frontend needed yet.

---

### Phase 3 — Browser Frontend (Planned)

**Goal:** A browser interface to interact with the API.

**Deliverables:**
- `index.html` — form for new entries, filter bar, log table, stats panel
- `style.css` — clean layout using Flexbox/Grid
- `app.js` — fetch calls, DOM rendering, filter logic, no framework

**Done when:** The whole app works in the browser — log a session, see it in the table, filter by category, and see updated stats, all without touching the terminal.

---

## The App: Logged

### What it does

- Log study sessions with a title, subject, category, context (personal / school / work), and duration
- Optionally rate each session: difficulty (1–10), usefulness (low / medium / high), enjoyment (emoji scale)
- Filter and search log history by category, context, or date range
- View statistics: total hours, breakdowns by category, most studied subject, average difficulty

### Data Model

Table: `learning_logs`

| Column | Type | Notes |
|--------|------|-------|
| `id` | INTEGER | Primary key, auto-incremented |
| `title` | TEXT | e.g. "FastAPI routing" |
| `notes` | TEXT | Optional longer description |
| `subject` | TEXT | e.g. "Python", "French", "Calculus" |
| `context` | TEXT | `private` / `school` / `work` |
| `category` | TEXT | See valid values below |
| `duration_minutes` | INTEGER | Session length |
| `difficulty` | INTEGER | Optional. 1–10 |
| `usefulness` | TEXT | Optional. `low` / `medium` / `high` |
| `enjoyment` | TEXT | Optional. `😴` / `😐` / `🙂` / `🤩` |
| `logged_at` | TEXT | Date of session (YYYY-MM-DD) |
| `created_at` | TEXT | Record insertion timestamp |

**Valid categories:** `programming`, `ai_ml`, `language`, `math`, `science`, `cars_engines`, `history`, `art_design_music`, `business_finance`, `health_fitness`, `philosophy_psych`, `writing_literature`, `general_knowledge`, `other`

### API Endpoints

| Method | Route | What it does |
|--------|-------|-------------|
| GET | `/api/logs` | All log entries (supports filters) |
| POST | `/api/logs` | Create a new entry |
| GET | `/api/logs/{id}` | Single entry by ID |
| PUT | `/api/logs/{id}` | Update an entry |
| DELETE | `/api/logs/{id}` | Delete an entry |
| GET | `/api/stats` | Summary statistics |

### Tech Stack

| Layer | Tool | Reason |
|-------|------|--------|
| Language | Python 3.x | Foundation — already known |
| Database | SQLite via `sqlite3` | No install, single file, SQL transfers to PostgreSQL 1:1 |
| Backend | FastAPI + Uvicorn | Modern, readable, auto-generates `/docs` for free |
| Validation | Pydantic | Bundled with FastAPI, validates request data automatically |
| Frontend | HTML5 + CSS3 + Vanilla JS (React) | No framework in the beginning, understand every line before abstracting. React as a v2.0 at a later stage when the HTML CSS JS basics are understood |

---

## What I Will Know When This Is Done

- How to design a relational data model from scratch
- How to write and organize SQL queries inside Python
- How a REST API works — HTTP methods, routes, request/response cycle
- How HTTP communication works between a browser and a server
- How to validate incoming data before it reaches the database
- How JavaScript talks to a backend without a page reload (`fetch`, DOM, event listeners)
- How to structure a multi-file project cleanly

These are the exact foundations expected in any junior web development role.

---

## Running the App (Phase 2+)

```bash
# Install dependencies
pip install fastapi uvicorn pydantic

# Set up the database (run once)
python learning_tracker/schema.py

# Start the server
uvicorn learning_tracker.main:app --reload

# Open the interactive API docs
# http://localhost:8000/docs

# Open the frontend
# http://localhost:8000
```
*This project will contain AI generated content! BUT the main goal is to use it as a tool for learning and really UNDERSTANDING the concepts and technologies used to create this it.*