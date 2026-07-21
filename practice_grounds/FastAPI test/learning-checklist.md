# JS + DOM Learning Checklist (for Quote Library frontend)

Goal: connect `index.html` to `main.py` (FastAPI) with vanilla JS — GET quotes, display them, then POST/PUT/DELETE.

## 1. DOM basics
- [ ] What the DOM is (browser's live tree built from HTML)
- [ ] `document.getElementById`
- [ ] `document.querySelector` / `querySelectorAll`
- [ ] `.textContent` vs `.innerHTML` (why `.textContent` is safer)
- [ ] `document.createElement`
- [ ] `.appendChild` / `.append`
- [ ] `.setAttribute`
- [ ] `.classList.add` / `.remove` / `.toggle`

## 2. JS fundamentals
- [ ] `let` vs `const`
- [ ] Functions and arrow functions
- [ ] Objects and arrays
- [ ] Looping over objects: `for...in`, `Object.entries`
- [ ] Array methods: `.map`, `.forEach`
- [ ] Template literals: `` `${variable}` ``

## 3. Events
- [ ] `addEventListener`
- [ ] Reading input values (`.value`)
- [ ] Preventing default form submission (`event.preventDefault()`)

## 4. Async JS / talking to the API
- [ ] `fetch()` basics
- [ ] `.then()` chains
- [ ] `async` / `await`
- [ ] `response.json()`
- [ ] `try/catch` error handling
- [ ] Checking `response.ok` / status codes

## 5. HTTP / API concepts
- [ ] GET vs POST vs PUT vs DELETE
- [ ] Setting method/headers/body in `fetch`
- [ ] Status codes (200, 404, etc.) and handling them on the frontend
- [ ] CORS — what it is, why it blocks local file → API requests, how to enable via `CORSMiddleware`

## 6. Polish (after core functionality works)
- [ ] Styling dynamically injected content with CSS
- [ ] Basic form validation

## Suggested build order for this project
1. Add CORS middleware to `main.py`
2. `fetch('/quotes')` and `console.log` the result (no UI yet)
3. Render fetched quotes into the empty `<p id="quote-of-the-day">` placeholder
4. Add a button + event listener to fetch a new/random quote
5. Build a form to POST a new quote
6. Add edit (PUT) and delete (DELETE) actions


do not focus too much on everything do html first, js next and css last.