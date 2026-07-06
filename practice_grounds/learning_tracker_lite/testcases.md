# Swagger UI Test Cases — logged lite API

Run these at `http://127.0.0.1:8000/docs` after starting the server with `uvicorn main:app --reload`.

---

## 1. GET `/` — Welcome message

**Steps:** Click **Try it out** → **Execute**

**Expected:** `200 OK`
```json
{ "message": "Welcome to the API of the logged lite app!" }
```

---

## 2. POST `/logs` — Create a valid entry

**Steps:** Click **Try it out**, paste the body below → **Execute**

**Request body:**
```json
{
  "subject": "FastAPI",
  "key_learnings": "Learned how to use Depends() for DB injection",
  "notes": "Check lifespan context manager docs",
  "time_spent": 1.5,
  "difficulty": 3
}
```

**Expected:** `201 Created`
```json
{
  "added successfully": {
    "subject": "FastAPI",
    "key_learnings": "Learned how to use Depends() for DB injection",
    "notes": "Check lifespan context manager docs",
    "time_spent": 1.5,
    "difficulty": 3
  }
}
```

---

## 3. POST `/logs` — Create entry using default notes value

**Steps:** Omit the `notes` field → **Execute**

**Request body:**
```json
{
  "subject": "SQLite",
  "key_learnings": "Practiced raw SQL queries and commits",
  "time_spent": 0.75,
  "difficulty": 2
}
```

**Expected:** `201 Created` — response should show `"notes": "no notes"`

---

## 4. POST `/logs` — Validation error (missing required field)

**Steps:** Send a body without `subject` → **Execute**

**Request body:**
```json
{
  "key_learnings": "Missing subject field",
  "time_spent": 1.0,
  "difficulty": 1
}
```

**Expected:** `422 Unprocessable Entity` — FastAPI validation error listing the missing `subject` field.

---

## 5. GET `/logs` — Retrieve all entries

**Steps:** Click **Try it out** → **Execute** (run after test cases 2 and 3)

**Expected:** `200 OK` — a dictionary keyed by entry ID containing all entries, e.g.:
```json
{
  "1": {
    "subject": "FastAPI",
    "key_learnings": "Learned how to use Depends() for DB injection",
    "notes": "Check lifespan context manager docs",
    "time_spent": 1.5,
    "difficulty": 3,
    "datetime": "..."
  }
}
```

---

## 6. GET `/logs/{entry_id}` — Retrieve a single entry

**Steps:** Set `entry_id` to `1` → **Execute**

**Expected:** `200 OK`
```json
{
  "id": 1,
  "subject": "FastAPI",
  "key_learnings": "Learned how to use Depends() for DB injection",
  "notes": "Check lifespan context manager docs",
  "time_spent": 1.5,
  "difficulty": 3,
  "datetime": "..."
}
```

---

## 7. GET `/logs/{entry_id}` — Entry not found

**Steps:** Set `entry_id` to `9999` → **Execute**

**Expected:** `404 Not Found`
```json
{ "detail": "This entry does not exist, please double check the id" }
```

---

## 8. PUT `/logs/{entry_id}` — Full update of an existing entry

**Steps:** Set `entry_id` to `1`, paste the body below → **Execute**

**Request body:**
```json
{
  "subject": "FastAPI (updated)",
  "key_learnings": "Also learned about response status codes",
  "notes": "Re-read the Response object docs",
  "time_spent": 2.0,
  "difficulty": 4
}
```

**Expected:** `200 OK` — response shows the updated entry fields.

---

## 9. PUT `/logs/{entry_id}` — Update non-existent entry

**Steps:** Set `entry_id` to `9999`, use any valid body → **Execute**

**Expected:** `404 Not Found`
```json
{ "detail": "This entry does not exist, please double check the id" }
```

---

## 10. DELETE `/logs/{entry_id}` — Delete an existing entry

**Steps:** Set `entry_id` to `2` (created in test 3) → **Execute**

**Expected:** `200 OK`
```json
{ "message": "entry with id 2, deleted successfuly" }
```

---

## 11. DELETE `/logs/{entry_id}` — Delete non-existent entry

**Steps:** Set `entry_id` to `9999` → **Execute**

**Expected:** `404 Not Found`
```json
{ "detail": "This entry does not exist, please double check the id" }
```

---

## Suggested run order

1. Test 1 (root check)
2. Test 2 (create entry → ID 1)
3. Test 3 (create entry with default notes → ID 2)
4. Test 4 (validation error)
5. Test 5 (get all — should see 2 entries)
6. Test 6 (get entry 1)
7. Test 7 (get missing entry)
8. Test 8 (update entry 1)
9. Test 9 (update missing entry)
10. Test 10 (delete entry 2)
11. Test 11 (delete missing entry)
