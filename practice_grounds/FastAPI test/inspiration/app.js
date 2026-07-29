// ---------------------------------------------------------------
// Quote Library -- shared frontend script
//
// This ONE file is loaded by all 6 HTML pages (see the
// <script src="app.js"></script> at the bottom of each page).
//
// Since you know Python: think of this file as running top-to-bottom
// once, like a Python script -- but instead of running via
// `python app.py`, the browser runs it after the HTML has loaded.
//
// Each page only has some of the elements this file looks for (e.g.
// only landingpage.html has a button with id="connectBtn"). So every
// section below does:
//
//     const thing = document.getElementById("someId");
//     if (thing) { ...set up behaviour for that page only... }
//
// document.getElementById(...) returns `null` if no element with that
// id exists on the current page. `if (thing)` is JS's way of checking
// "is this truthy?" -- null is falsy, so the block is skipped. This
// is roughly like doing:
//
//     thing = soup.find(id="someId")   # BeautifulSoup-ish
//     if thing is not None:
//         ...
//
// It means this single script can be safely included on every page
// without crashing on pages that don't have a given element.
// ---------------------------------------------------------------

// A plain variable holding the API's base URL, so we don't repeat
// "http://127.0.0.1:8000" everywhere. `const` means this binding can't
// be reassigned later -- like a constant, though (like Python) it
// doesn't stop you from mutating an object's *contents*, just from
// pointing the name at something else.
const API_BASE = "http://127.0.0.1:8000";

// ---------------------------------------------------------------
// Helper 1: showStatus
// Small reusable function so every page can show a colored
// success/error/info message the same way, instead of repeating this
// logic 6 times. Equivalent to writing a little helper function at
// the top of a Python script and calling it from multiple places.
// ---------------------------------------------------------------
function showStatus(el, message, type = "info") {
  // `type = "info"` is a default parameter value, same idea as
  // Python's `def showStatus(el, message, type="info"):`.

  if (!el) return;
  // `!el` means "not el" (logical NOT). If no element was passed in
  // (e.g. this page doesn't have a status paragraph), just exit early
  // instead of crashing. Same as `if el is None: return` in Python.

  el.textContent = message;
  // .textContent sets the plain text inside an HTML element, e.g. the
  // text between <p id="foo"> and </p>. It's the safe alternative to
  // .innerHTML (more on that further down).

  el.className = `status-message ${type}`;
  // Backticks make a "template literal" -- JS's f-string. This is the
  // same as Python's f"status-message {type}". It sets the element's
  // CSS class, e.g. class="status-message error", which style.css
  // uses to color it red/green/grey.

  el.classList.remove("hidden");
  // Our CSS has a `.hidden { display: none; }` rule. Removing that
  // class makes a previously-hidden message visible.
}

// ---------------------------------------------------------------
// Helper 2: apiFetch
// Wraps the browser's built-in `fetch()` function (the JS equivalent
// of Python's `requests.get()` / `requests.post()`) so every API call
// in this file handles errors the exact same way.
// ---------------------------------------------------------------

// `async function` marks this function as asynchronous -- it can use
// `await` inside it, and calling it always gives you back a "Promise"
// (JS's version of something you can await, similar in spirit to an
// `async def` coroutine in Python's asyncio). Every place that calls
// apiFetch() must also use `await` or `.then()` to get the actual result.
async function apiFetch(path, options = {}) {
  // `options = {}` defaults to an empty object -- same idea as Python
  // `def apiFetch(path, options=None): options = options or {}`.
  // `options` can carry things like { method: "POST", body: ... }.

  const response = await fetch(`${API_BASE}${path}`, options);
  // fetch() sends the HTTP request and returns a Promise that resolves
  // once the response headers have arrived (the body may still be
  // streaming in). `await` pauses this function until that happens --
  // similar to `response = await client.get(url)` if you've used
  // Python's httpx/aiohttp in async mode. Nothing else in the browser
  // freezes while we wait; JS just moves on to other work and comes
  // back here when the response is ready.

  const data = await response.json().catch(() => null);
  // response.json() reads the response body and parses it as JSON --
  // like Python's `response.json()` in requests, except here it's
  // ALSO async (the body has to be read from the network first), so
  // it needs its own `await`.
  // .catch(() => null) means: if parsing fails (e.g. the server sent
  // no body, or broken JSON), don't crash -- just use `null` instead.
  // `() => null` is an arrow function that takes no arguments and
  // always returns null (see the note on arrow functions below).

  if (!response.ok) {
    // response.ok is a boolean: true for status codes 200-299, false
    // for anything else (404, 500, etc). This is different from
    // Python's requests, where you'd typically check
    // `response.status_code` or call `response.raise_for_status()`.
    const detail = data && data.detail ? data.detail : response.statusText;
    // FastAPI's HTTPException puts its message in a "detail" field,
    // e.g. {"detail": "Quote not found"}. This line says: "if `data`
    // exists AND `data.detail` exists, use it; otherwise fall back to
    // the generic HTTP status text (like 'Not Found')."
    // This `a && b ? b : c` pattern is JS's compact way of writing
    // Python's `data.detail if data and data.detail else response.statusText`.

    throw new Error(detail);
    // `throw` raises an exception, just like Python's `raise`.
    // `new Error(...)` builds a JS Error object, roughly analogous to
    // `raise Exception(detail)`. Whoever called apiFetch() needs a
    // try/catch around it to handle this (see below).
  }

  return data;
}

// ---------------------------------------------------------------
// Landing page: "test connection" button
// (Only landingpage.html has #connectBtn, so this whole block is a
// no-op on every other page.)
// ---------------------------------------------------------------

const connectBtn = document.getElementById("connectBtn");
if (connectBtn) {
  const welcomeMessage = document.getElementById("welcomeMessage");
  const apiAuthor = document.getElementById("apiAuthor");

  connectBtn.addEventListener("click", async () => {
    // addEventListener registers a function to run when an event
    // happens -- here, "click". This is JS's equivalent of wiring up
    // a callback, e.g. like `button.on_click(handler)` in a GUI
    // framework such as tkinter.
    //
    // `async () => { ... }` is an "arrow function" -- a compact way
    // to write a function, similar to Python's `lambda`, except arrow
    // functions CAN contain multiple statements and `return`, not
    // just a single expression. `async` lets us `await` inside it.
    // Roughly: async def handler(): ...

    try {
      const data = await apiFetch("/");
      // Calls our helper above. GET / on the API returns
      // {"Message": ..., "Built_by": ...} per main.py.

      welcomeMessage.textContent = data.Message;
      apiAuthor.textContent = "Built by " + data.Built_by;
      // `+` on strings concatenates them, same as Python.
    } catch (error) {
      // try/except in JS is try/catch -- same idea, different keyword.
      // If apiFetch() threw (e.g. server not running, or a 404), we
      // land here instead of crashing the page.
      welcomeMessage.textContent = "Could not reach the API.";
      apiAuthor.textContent = error.message;
      // `error.message` is the string we passed to `new Error(...)`
      // earlier -- like Python's `str(exception)`.
    }
  });
}

// ---------------------------------------------------------------
// Show all quotes page
// (Only showAllQuotes.html has #quoteList.)
// ---------------------------------------------------------------

const quoteList = document.getElementById("quoteList");
if (quoteList) {
  const statusEl = document.getElementById("listStatus");

  // A regular (non-async) helper: turns ONE quote object, e.g.
  // { id: 1, quote: "...", author: "...", year: 2026 }, into an
  // actual HTML element we can insert into the page.
  //
  // This uses document.createElement + .textContent instead of just
  // building an HTML string, on purpose: if a quote's text ever
  // contained something like "<script>...</script>", .textContent
  // would display it as literal, harmless text, whereas stuffing it
  // into .innerHTML would make the browser try to run it as real
  // HTML/JS. This class of bug is called XSS (cross-site scripting).
  // Building elements piece-by-piece like this avoids it entirely.
  function renderQuoteCard(q) {
    const item = document.createElement("div");
    // Creates a new, empty <div></div> -- not yet attached to the
    // page. Comparable to building an object in memory before you
    // decide where it goes, e.g. `el = Element("div")`.
    item.className = "quote-item"; // matches the .quote-item CSS rule

    const blockquote = document.createElement("blockquote");
    blockquote.textContent = q.quote;
    // q.quote reads the "quote" key off the object -- JS uses dot
    // notation for dict-like access where Python would use
    // q["quote"] (JS objects behave like a mix of a Python dict and
    // a namespace; dot access is the normal idiom).

    const meta = document.createElement("div");
    meta.className = "quote-meta";

    const authorYear = document.createElement("span");
    authorYear.textContent = `${q.author} · ${q.year}`;
    // Template literal again (f-string equivalent): "Author · 2026".

    const idBadge = document.createElement("span");
    idBadge.className = "id-badge";
    idBadge.textContent = `#${q.id}`;

    meta.append(authorYear, idBadge);
    // .append(...) inserts children into a parent element. You can
    // pass multiple elements at once, like a Python list.extend()
    // but for the DOM tree. Order here = left-to-right in the HTML.

    item.append(blockquote, meta);
    return item;
    // We hand back the fully-built <div> so the caller can decide
    // where to put it (see loadQuotes below).
  }

  async function loadQuotes() {
    try {
      const quotes = await apiFetch("/quotes");
      // main.py's GET /quotes now returns a JSON *array* of quote
      // objects (see the README for why), so `quotes` here is a JS
      // array -- basically a Python list of dicts.

      quoteList.innerHTML = "";
      // Clears out whatever was inside #quoteList before (the
      // "Loading..." placeholder text from the HTML). Setting
      // innerHTML = "" is safe here because we're not inserting any
      // *new* untrusted content this way -- just wiping it blank.

      if (quotes.length === 0) {
        // JS arrays use `.length`, not Python's `len(quotes)`.
        showStatus(statusEl, "No quotes yet -- go create one!", "info");
        return;
      }

      statusEl.classList.add("hidden"); // hide the "Loading..." message
      quotes.forEach((q) => quoteList.appendChild(renderQuoteCard(q)));
      // .forEach(callback) runs `callback` once per array item --
      // JS's version of `for q in quotes: ...`. `(q) => ...` is
      // another arrow function: "for each quote q, do this."
      // .appendChild adds a single element as the last child of
      // #quoteList (like .append() above, but for exactly one node).
    } catch (error) {
      showStatus(statusEl, `Failed to load quotes: ${error.message}`, "error");
    }
  }

  loadQuotes();
  // Actually call the function we just defined -- this runs
  // immediately when the page (and this script) loads, which is why
  // the quote list appears without you having to click anything.
}

// ---------------------------------------------------------------
// Show a single quote by ID (+ random quote button)
// (Only showSpecificQuote.html has #showQuoteForm.)
// ---------------------------------------------------------------

const showQuoteForm = document.getElementById("showQuoteForm");
if (showQuoteForm) {
  const idInput = document.getElementById("showQuoteId");
  const resultEl = document.getElementById("singleQuoteResult");
  const randomBtn = document.getElementById("randomQuoteBtn");

  function displayQuote(q) {
    resultEl.innerHTML = "";
    const item = document.createElement("div");
    item.className = "quote-item";
    item.innerHTML = `
      <blockquote>${escapeHtml(q.quote)}</blockquote>
      <div class="quote-meta">
        <span>${escapeHtml(q.author)} · ${q.year}</span>
        <span class="id-badge">#${q.id}</span>
      </div>
    `;
    // Here we DO use innerHTML with a template literal, because it's
    // much less code than building 5 elements by hand with
    // createElement. But that means any quote text gets interpreted
    // as HTML markup unless we neutralise it first -- that's exactly
    // what escapeHtml() below does to q.quote and q.author before
    // they're dropped into this string. q.id and q.year are numbers
    // from our own trusted API, so they don't need escaping.
    resultEl.appendChild(item);
  }

  // Turns any string into a "safe" version where HTML-special
  // characters like < > & are converted to their harmless text
  // equivalents (&lt; &gt; &amp;). The trick: assign the string to
  // .textContent (which never interprets HTML), then read back
  // .innerHTML (which gives us the escaped version as text). It's a
  // neat built-in-browser way to escape HTML without writing your own
  // find-and-replace logic.
  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  showQuoteForm.addEventListener("submit", async (event) => {
    // "submit" fires when the <form> is submitted -- by clicking its
    // button, or pressing Enter in one of its inputs.
    event.preventDefault();
    // By default, submitting a form makes the browser navigate to a
    // new page (a full page reload) and send the data the old-school
    // way. Since we want to handle everything ourselves with fetch(),
    // we cancel that default behaviour. Forgetting this line is one
    // of the most common beginner JS bugs -- the page just refreshes
    // and nothing seems to happen.

    try {
      const quote = await apiFetch(`/quotes/${idInput.value}`);
      // idInput.value reads whatever the user typed into the number
      // input, as a string. Template literal builds the URL, e.g.
      // "/quotes/3". FastAPI converts that string to an int for us
      // based on the `quote_id: int` type hint in main.py -- if it's
      // not a valid int, FastAPI itself returns a 422 error, which
      // apiFetch() will turn into a thrown Error.
      displayQuote(quote);
    } catch (error) {
      showStatus(resultEl, error.message, "error");
    }
  });

  if (randomBtn) {
    // Extra safety check even though this page always has the
    // button -- cheap insurance, and shows the same guard pattern
    // used everywhere else in this file.
    randomBtn.addEventListener("click", async () => {
      try {
        const quote = await apiFetch("/quotes/random");
        idInput.value = quote.id;
        // Also fill the number input with the ID we landed on, so
        // the user can see which quote they got.
        displayQuote(quote);
      } catch (error) {
        showStatus(resultEl, error.message, "error");
      }
    });
  }
}

// ---------------------------------------------------------------
// Create a new quote
// (Only createNewQuote.html has #createQuoteForm.)
// ---------------------------------------------------------------

const createQuoteForm = document.getElementById("createQuoteForm");
if (createQuoteForm) {
  const statusEl = document.getElementById("createStatus");

  createQuoteForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const quote = document.getElementById("newQuote").value.trim();
    // .trim() strips leading/trailing whitespace, same as Python's
    // .strip().
    const author = document.getElementById("newQuoteAuthor").value.trim() || "Unknown";
    // `a || b` means "a if a is truthy, otherwise b" -- JS's version
    // of Python's `a or b`. Empty string "" is falsy in JS (like in
    // Python), so if the author field was left blank, this falls
    // back to "Unknown".
    const year = Number(document.getElementById("newQuoteYear").value) || 2026;
    // Number(...) converts a string to a number, like Python's
    // int()/float(). If the field was blank, Number("") is 0, which
    // is falsy, so `|| 2026` supplies our default.

    if (!quote) {
      showStatus(statusEl, "Quote text can't be empty.", "error");
      return;
      // `return` with no value just exits the function early --
      // same as a bare `return` in Python.
    }

    try {
      const created = await apiFetch("/quotes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ quote, author, year }),
        // { quote, author, year } is "shorthand property syntax" --
        // when the key name and variable name match, JS lets you
        // skip writing `quote: quote`. It's exactly the same as
        // writing { quote: quote, author: author, year: year }.
        // JSON.stringify converts that JS object into a JSON string
        // for the request body, like Python's json.dumps(). We also
        // have to explicitly say Content-Type: application/json so
        // FastAPI knows to parse the body as JSON.
      });
      showStatus(statusEl, `Created quote #${created.id}.`, "success");
      createQuoteForm.reset();
      // .reset() clears all the form's inputs back to empty, so the
      // user can immediately type another quote.
    } catch (error) {
      showStatus(statusEl, `Failed to create quote: ${error.message}`, "error");
    }
  });
}

// ---------------------------------------------------------------
// Edit an existing quote
// Two-step flow: load quote by ID into the form, then submit to save.
// (Only changeQuote.html has #loadQuoteForm.)
// ---------------------------------------------------------------

const loadQuoteForm = document.getElementById("loadQuoteForm");
if (loadQuoteForm) {
  const idInput = document.getElementById("editQuoteId");
  const editFields = document.getElementById("editFields");
  const editForm = document.getElementById("editQuoteForm");
  const statusEl = document.getElementById("editStatus");

  const quoteInput = document.getElementById("editQuoteText");
  const authorInput = document.getElementById("editQuoteAuthor");
  const yearInput = document.getElementById("editQuoteYear");

  // Step 1: "Load quote" form -- fetches the current quote and fills
  // the (initially hidden) edit form with its values.
  loadQuoteForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const q = await apiFetch(`/quotes/${idInput.value}`);
      quoteInput.value = q.quote;
      authorInput.value = q.author;
      yearInput.value = q.year;
      // Setting .value on an <input>/<textarea> is how you fill it
      // in with JS -- like typing into it programmatically.

      editFields.classList.remove("hidden");
      // Reveals the second card (the actual edit form) now that we
      // have data to show in it.
      statusEl.classList.add("hidden");
    } catch (error) {
      editFields.classList.add("hidden");
      showStatus(statusEl, error.message, "error");
    }
  });

  // Step 2: "Save changes" form -- sends the edited values back with
  // PUT, which in main.py fully replaces the stored quote at that id.
  editForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      await apiFetch(`/quotes/${idInput.value}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          quote: quoteInput.value.trim(),
          author: authorInput.value.trim() || "Unknown",
          year: Number(yearInput.value) || 2026,
        }),
      });
      showStatus(statusEl, `Quote #${idInput.value} updated.`, "success");
    } catch (error) {
      showStatus(statusEl, `Failed to update quote: ${error.message}`, "error");
    }
  });
}

// ---------------------------------------------------------------
// Delete a quote
// (Only deleteQuote.html has #deleteQuoteForm.)
// ---------------------------------------------------------------

const deleteQuoteForm = document.getElementById("deleteQuoteForm");
if (deleteQuoteForm) {
  const idInput = document.getElementById("deleteQuoteId");
  const statusEl = document.getElementById("deleteStatus");

  deleteQuoteForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    try {
      const result = await apiFetch(`/quotes/${idInput.value}`, { method: "DELETE" });
      // DELETE requests normally have no body, so we only pass
      // { method: "DELETE" } -- no headers/body needed here.
      showStatus(statusEl, `${result.message} (id ${result.removed_quote_id}).`, "success");
      deleteQuoteForm.reset();
    } catch (error) {
      showStatus(statusEl, `Failed to delete quote: ${error.message}`, "error");
    }
  });
}
