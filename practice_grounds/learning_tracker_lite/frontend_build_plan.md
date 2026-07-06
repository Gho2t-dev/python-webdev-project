# Frontend Build Plan — Logged Lite

## What You're Building

A browser UI that talks to your existing FastAPI backend. The user sees log entries, can add new ones, edit them, and delete them — all without touching the terminal.

---

## The Mental Model

Your backend is already done. It exposes a REST API at `http://localhost:8000`. The frontend's entire job is:

1. **Fetch** data from the API and render it as HTML
2. **Collect** user input via forms and send it back to the API

The browser does this using **JavaScript's `fetch()` function**, which lets you make HTTP requests (GET, POST, PUT, DELETE) from inside a webpage — just like you did with curl or the Swagger UI.

---

## Tech Stack (Keep It Simple)

No React, no Vue, no build tools. Just three files the browser already understands:

| File | Purpose |
|------|---------|
| `index.html` | Structure — what exists on the page |
| `style.css` | Appearance — how it looks |
| `app.js` | Behavior — what it does |

This is called **Vanilla JS**. It's slower to write at scale, but it teaches you *exactly* what frameworks hide from you. Once you understand this, React will make sense.

---

## Step-by-Step Build Plan

### Step 1 — Scaffold the HTML (`index.html`)

Create three sections:
- A **header** with the app title
- A **list section** to display all entries (empty at first, JS fills it)
- A **form section** with inputs for subject, key_learnings, notes, time_spent, and difficulty

Key concepts to learn here:
- HTML form elements: `<input>`, `<textarea>`, `<button>`
- `id` attributes — JS will find elements by these
- `<div>` containers for grouping

---

### Step 2 — Load All Entries on Page Load (`app.js`)

Write a function `loadEntries()` that:
1. Calls `fetch('http://localhost:8000/logs')` — this is a GET request
2. Parses the JSON response with `.json()`
3. Loops over the entries and builds HTML strings for each
4. Injects them into your list section using `innerHTML` or `appendChild`

Then call `loadEntries()` at the bottom of the file so it runs when the page opens.

Key concepts to learn here:
- `async/await` — fetch is asynchronous (it waits for a network response)
- `.then()` chains as the alternative syntax
- Manipulating the DOM with `document.getElementById()` and `innerHTML`

---

### Step 3 — Add the Create Form (`app.js`)

Write a function `createEntry()` that:
1. Reads values from the form inputs using `document.getElementById('subject').value`
2. Builds a JSON object matching your `NewEntry` model
3. Calls `fetch('http://localhost:8000/logs', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) })`
4. On success, clears the form and calls `loadEntries()` to refresh the list

Attach this to the form's submit button using an event listener:
```js
document.getElementById('submit-btn').addEventListener('click', createEntry)
```

Key concepts to learn here:
- `fetch()` with options object (method, headers, body)
- `JSON.stringify()` to convert JS object → JSON string
- Event listeners

---

### Step 4 — Add Delete Buttons

Inside your `loadEntries()` loop, add a Delete button to each entry's HTML. Give it a `data-id` attribute set to the entry's ID:

```html
<button class="delete-btn" data-id="3">Delete</button>
```

Then add a single event listener on the list container that catches all button clicks (this is called **event delegation**):

```js
document.getElementById('log-list').addEventListener('click', function(e) {
    if (e.target.classList.contains('delete-btn')) {
        const id = e.target.dataset.id
        fetch(`http://localhost:8000/logs/${id}`, { method: 'DELETE' })
            .then(() => loadEntries())
    }
})
```

Key concepts to learn here:
- `data-*` attributes for embedding data in HTML
- Event delegation — one listener handles many buttons
- Template literals (backtick strings) for building URLs

---

### Step 5 — Add Edit / Update

This is the hardest step. Two approaches:

**Option A (simpler):** When the user clicks Edit, replace the entry's text with pre-filled inputs and a Save button. On Save, send a PUT request.

**Option B (modal):** Pop up a form overlay. More polished but more DOM work.

Start with Option A. A PUT request looks like POST but uses `method: 'PUT'` and targets `/logs/{id}`.

---

### Step 6 — Handle CORS

When you open `index.html` directly from the file system and it tries to call `localhost:8000`, the browser will likely block it with a **CORS error**. This is a browser security rule.

Fix it in your FastAPI backend by adding:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this in production
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Key concept to understand: CORS (Cross-Origin Resource Sharing) — the browser only allows a webpage to call APIs on the same "origin" (domain + port) unless the server explicitly allows it.

---

### Step 7 — Serve the Frontend (Optional but Clean)

Instead of opening `index.html` as a file, you can serve it through FastAPI itself:

```python
from fastapi.staticfiles import StaticFiles
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
```

This makes `http://localhost:8000` serve your HTML, which also solves CORS automatically since everything is the same origin.

---

## Suggested Build Order

1. `index.html` skeleton with hard-coded dummy entry (no JS yet)
2. Add `style.css` and make it look decent
3. `app.js` — `loadEntries()` only, confirm entries load from API
4. Add create form + `createEntry()`
5. Add delete buttons
6. Add edit/update flow
7. Add CORS middleware to backend
8. (Optional) Serve frontend via FastAPI static files

Build one step, test it, then move on. Do not try to write all the JS at once.

---

## Key JavaScript Concepts to Study First

If any of these are unfamiliar, read about them before you start coding:

- `async/await` and Promises
- `fetch()` API
- DOM selection: `document.getElementById`, `querySelector`
- DOM manipulation: `innerHTML`, `appendChild`, `createElement`
- Event listeners: `addEventListener('click', fn)`
- Template literals: `` `Hello ${name}` ``
- `JSON.stringify()` and `JSON.parse()`

MDN Web Docs (developer.mozilla.org) is the best reference for all of these.

---

## What Success Looks Like

When you're done, opening the app in a browser lets you:
- See all log entries listed on screen
- Fill out a form to add a new one
- Click Delete to remove one
- Click Edit to update one

No terminal commands needed by the end user.
