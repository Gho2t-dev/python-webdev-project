# Full-Stack Learning Journey — Python Web Development

A documented learning path from Python fundamentals to a fully self-built, full-stack web application. Every file in this repo is a step toward one goal: building a personal learning tracker app called **Logged** — a real tool I will actually use, built entirely from scratch.

---

## The Goal

Build a full-stack web application called **Logged** where I can log study sessions, track time spent per subject, rate difficulty and usefulness, and see statistics about my learning habits over time.

This is not a tutorial project. It is a real app with a real data model, a real REST API, and a real browser UI — built by learning each layer of the stack from the ground up.

## My Background

I am a 22 year old engineer / engineering student from Switzerland. I work in a power semiconductor production plant where I maintain semiconductor production equipment. I studied for 4 years to get the "EFZ" as Automation Technician. I am currently working on my Professional Bachelor's Degree in Systems Engineering at ABBTS.

---

## Repository Structure

```
python-webdev-project/
├── practice_grounds/                     # Everything practiced before touching the real "Logged" build
│   ├── sql_basics.py                     # SQLite fundamentals (connect, create, insert)
│   ├── SQLite_Practice.py                # Early SQLite experiments
│   ├── OOP_Example_Code.py               # First look at OOP: classes, inheritance, polymorphism
│   ├── Database Viewer v1.0.py           # First real, self-made CLI app: CRUD on a SQLite database
│   │
│   ├── Webdev Basics/                    # Raw HTML / CSS / JS fundamentals
│   │   ├── HTML Practice/                # First HTML pages, structure, media embedding
│   │   ├── CSS Practice/                 # Flexbox/Grid layout practice
│   │   └── JavaScript Practice/          # DOM, events, ternary, switch, counters, random numbers
│   │
│   ├── FastAPI test/                     # First backend + frontend wiring test ("Quote Library")
│   │   ├── main.py                       # First FastAPI app with CRUD endpoints
│   │   ├── index.html / app.js / style.css
│   │   └── learning-checklist.md         # DOM/fetch/HTTP concept checklist used to learn JS-to-API wiring
│   │
│   └── learning_tracker_lite/            # Full dry-run of the "Logged" build — smaller schema, same phases
│       ├── database.py                   # Phase 1: CRUD + init_db functions
│       ├── main.py                       # Phase 2: FastAPI app, Pydantic validation, lifespan-managed DB
│       ├── logged_lite.py                # Standalone CLI precursor to the API version
│       ├── testcases.md                  # Manual Swagger UI test plan for every endpoint
│       ├── Database concept.md           # Simplified data model + planning notes
│       ├── frontend_build_plan.md        # Step-by-step vanilla JS frontend plan
│       └── index.html / app.js / style.css   # Phase 3: frontend (skeleton stage)
│
├── learning_tracker_proposal_by_AI.md    # Full project spec and design rationale for "Logged"
└── .gitignore
```

> `learning_tracker_lite` is intentionally a smaller, throwaway version of "Logged" — same phases (DB → API → frontend), simpler schema (`subject`, `key_learnings`, `notes`, `time_spent`, `difficulty`), used to rehearse the full stack once before building the real thing.

---

## Learning Steps So Far

### 1. Python & SQLite foundations
- [`sql_basics.py`](practice_grounds/sql_basics.py) — connecting to SQLite, creating tables, inserting rows with parameterized queries, fetching with filters, committing and closing connections
- [`SQLite_Practice.py`](practice_grounds/SQLite_Practice.py) — first contact with the `sqlite3` module and the cursor pattern
- [`OOP_Example_Code.py`](practice_grounds/OOP_Example_Code.py) — classes, `__init__`, instance attributes, encapsulation, inheritance, `super()`, method overriding, polymorphism, list comprehensions, modeled around an equipment maintenance system
- [`Database Viewer v1.0.py`](<practice_grounds/Database Viewer v1.0.py>) — first complete CLI app built end-to-end: interactive loop, input validation, parameterized SQL inserts/updates/deletes, persistent SQLite storage (iterated through many commits: add/edit/delete functionality, validation, stability and UX passes)

### 2. HTML / CSS / JavaScript basics (`Webdev Basics/`)
- **HTML Practice** — page structure, embedding media, multi-page navigation (`index.html`, `page2.html`, `ad.html`)
- **CSS Practice** — layout with Flexbox/Grid
- **JavaScript Practice** — a deliberate progression through core JS mechanics, each in its own folder:
  - `Basics` — variables, functions, fundamentals
  - `Math` — operators and numeric logic
  - `Ternary operator` — conditional expressions
  - `Switch Statements` — multi-branch control flow
  - `checked property` — reading/writing checkbox state via the DOM
  - `RandomNumber` — generating and displaying random values
  - `counter program` — first small interactive app combining state, DOM updates, and event listeners
- **Quote Library** (early commits) — first real mini-project combining HTML/CSS/JS: quote display section, layout styling, structural refactors

### 3. First backend + frontend wiring (`FastAPI test/` — "Quote Library" API)
- Built a first FastAPI app with full CRUD endpoints
- Used [`learning-checklist.md`](<practice_grounds/FastAPI test/learning-checklist.md>) to deliberately learn, in order: DOM basics → JS fundamentals → events → async JS/fetch → HTTP/API concepts (methods, status codes, CORS) → styling/validation polish
- Goal was purely to prove the wiring: browser JS talking to a Python API server, before attempting the larger tracker schema

### 4. Learning Tracker Lite — full dry run (`learning_tracker_lite/`)
A deliberately smaller version of the final "Logged" app, used to rehearse every phase once before the real build. Schema: `subject`, `key_learnings`, `notes`, `time_spent`, `difficulty`, auto `id` and `datetime` (see [`Database concept.md`](practice_grounds/learning_tracker_lite/Database%20concept.md)).

- **Phase 1 — Database layer** ✅ — [`database.py`](practice_grounds/learning_tracker_lite/database.py): `init_db`, add/edit/delete entry, fetch all/by-id, all using parameterized SQL
- **Phase 2 — FastAPI backend** ✅ — [`main.py`](practice_grounds/learning_tracker_lite/main.py): Pydantic `NewEntry` model with field validation (`Field(ge=1, le=10)` for difficulty, default values), lifespan-managed DB connection via `get_db()` dependency, full REST surface (`GET /`, `GET /logs`, `GET /logs/{id}`, `POST /logs`, `PUT /logs/{id}`, `DELETE /logs/{id}`), proper status codes (201, 404, 422) and error handling for missing entries
- **Testing** ✅ — [`testcases.md`](practice_grounds/learning_tracker_lite/testcases.md): full manual Swagger UI test plan covering happy paths, defaults, validation errors, and not-found cases for every endpoint, with a suggested run order
- **Phase 3 — Frontend** 🚧 in progress — [`frontend_build_plan.md`](practice_grounds/learning_tracker_lite/frontend_build_plan.md) lays out the step-by-step vanilla JS build (load entries → create form → delete buttons → edit/update → CORS → optional static-file serving). `index.html` has the header/section skeleton in place; `app.js`/`style.css` are the next step (`loadEntries()` first, per the plan)

**Why build this smaller version first?** To hit every concept — schema design, CRUD, Pydantic validation, REST routes, fetch/DOM wiring — once on a low-stakes project before repeating the same phases on "Logged" with its larger schema (context, category, usefulness, enjoyment, filtering, stats).

---

## Next Step

Finish Phase 3 of `learning_tracker_lite` (vanilla JS frontend: `loadEntries()`, create form, delete, edit/update, CORS), then carry every lesson from that dry run into building **Logged** for real, following the phases below.

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

## Project Phases (for "Logged")

### Phase 1 — Database Layer (Planned)

**Goal:** A Python module that handles all database operations. No web server yet.

**Deliverables:**
- `schema.py` — creates `app.db` and defines the `learning_logs` table
- `database.py` — CRUD functions plus a `get_stats()` aggregation query

**Done when:** Every function can be called from the terminal and data is correctly saved to and retrieved from `app.db`.

### Phase 2 — FastAPI Backend (Planned)

**Goal:** Wrap the Phase 1 database functions in an HTTP API server.

**Deliverables:**
- `main.py` — FastAPI app with Uvicorn, Pydantic validation models, CORS middleware
- All six REST endpoints wired to `database.py`

**Done when:** `http://localhost:8000/docs` is open and all endpoints work end-to-end through FastAPI's built-in UI — no custom frontend needed yet.

### Phase 3 — Browser Frontend (Planned)

**Goal:** A browser interface to interact with the API.

**Deliverables:**
- `index.html` — form for new entries, filter bar, log table, stats panel
- `style.css` — clean layout using Flexbox/Grid
- `app.js` — fetch calls, DOM rendering, filter logic, no framework

**Done when:** The whole app works in the browser — log a session, see it in the table, filter by category, and see updated stats, all without touching the terminal.

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

## Running Learning Tracker Lite (the practice build)

```bash
cd practice_grounds/learning_tracker_lite

# Install dependencies
pip install fastapi uvicorn pydantic

# Start the server (creates learning_tracker_lite.db on first run)
uvicorn main:app --reload

# Open the interactive API docs and run through testcases.md
# http://127.0.0.1:8000/docs
```

*This project will contain AI generated content! BUT the main goal is to use it as a tool for learning and really UNDERSTANDING the concepts and technologies used to create this it.*
