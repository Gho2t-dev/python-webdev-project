# Quote Library — Inspiration Version

This folder is a polished, fully-wired version of the Quote Library
project in the parent `FastAPI test/` folder. It exists purely as a
reference Compare the two to see
what changed and why.

## Running it

```bash
cd "practice_grounds/FastAPI test/inspiration"
source ../../../.venv/bin/activate
uvicorn main:app --reload
```

The API runs at `http://127.0.0.1:8000` (docs at `/docs`).

Then open `landingpage.html` through a local static server (e.g. VS
Code's "Live Server" extension), **not** by double-clicking the file.
Opening HTML directly as `file://` can cause `fetch()` requests to
behave inconsistently in some browsers — serving it over `http://`
avoids that entirely.

## Files

| File | Purpose |
|---|---|
| `main.py` | FastAPI backend — in-memory quote store, same data model as your original |
| `style.css` | One shared stylesheet used by every page |
| `app.js` | One shared script used by every page — all `fetch()` calls live here |
| `landingpage.html` | Home page + "test connection" button |
| `showAllQuotes.html` | Lists every quote (`GET /quotes`) |
| `showSpecificQuote.html` | Look up a quote by ID, or fetch a random one |
| `createNewQuote.html` | Form to add a quote (`POST /quotes`) |
| `changeQuote.html` | Load a quote by ID, then edit and save it (`PUT /quotes/{id}`) |
| `deleteQuote.html` | Delete a quote by ID (`DELETE /quotes/{id}`) |

## What changed vs. the original `main.py`

- **`GET /quotes` returns a list, not a dict.** A dict keyed by ID is
  awkward to loop over in JS (`Object.entries` + manual mapping). A
  list of `{id, quote, author, year}` objects is what `Array.map()` /
  `forEach()` expect, and it's what most real APIs do.
- **`response_model` on every route.** Tells FastAPI (and anyone
  reading `/docs`) exactly what shape comes back, and strips any
  accidental extra fields before they reach the client.
- **`GET /quotes/random` added.** Small, fun feature to demonstrate
  route ordering: it's declared *before* `/quotes/{quote_id}` in
  `main.py`, because FastAPI matches routes top-to-bottom and would
  otherwise try to parse `"random"` as an `int` and fail.
- **CORS opened to `*`.** Your original locked it to
  `http://127.0.0.1:5500` (Live Server's default port). `*` is fine
  for a local learning project with no cookies/auth involved — just
  don't do this in a real product.

## Frontend architecture notes

**One `app.js` for every page.** Rather than a separate script per
page, all the logic lives in one file. Each block starts with a DOM
lookup guarded by `if (element) { ... }`:

```js
const connectBtn = document.getElementById("connectBtn");
if (connectBtn) {
  // only runs on the page that actually has this button
}
```

This means the same `app.js` can be safely `<script>`-included on
every page without throwing errors on pages that don't have a given
element.

**A shared `apiFetch()` helper** wraps every request so all six pages
handle errors the same way — it checks `response.ok`, and if the
request failed, it reads FastAPI's `{"detail": "..."}` error shape and
throws a normal JS `Error` with that message. Every call site just
does:

```js
try {
  const data = await apiFetch("/quotes/5");
  // use data
} catch (error) {
  showStatus(statusEl, error.message, "error");
}
```

**`textContent` / `createElement` over `innerHTML`** wherever quote
text is inserted into the page. Setting `.textContent` can never be
interpreted as HTML, so a quote containing `<script>` or stray tags
can't break the page or run as code. `showSpecificQuote.html` needs
`innerHTML` for its template-string layout, so it escapes the quote
text first with a small `escapeHtml()` helper — worth reading in
`app.js` to see the difference between the two approaches.

**Two-step edit flow.** `changeQuote.html` first `GET`s the quote so
you can see current values, *then* reveals the edit form and `PUT`s
on save. This avoids silently overwriting fields the user didn't mean
to touch.

## Styling notes

Everything is in one `style.css` using CSS custom properties
(`:root { --primary: ...; }`) for colors, so the whole palette can be
changed by editing a handful of variables at the top of the file
instead of hunting through every rule. Layout is card-based (`.card`,
`.quote-item`) with a consistent shadow/radius applied via variables
too.

## Suggested next steps if you want to extend this yourself

- Swap the in-memory dict in `main.py` for JSON-file or SQLite
  persistence so quotes survive a server restart.
- Add client-side validation (e.g. don't allow a year before 1)
  before the form even submits.
- Add a loading spinner/disabled state on buttons while a `fetch()`
  is in flight.
