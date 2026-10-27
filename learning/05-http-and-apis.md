# Module 05 — HTTP and APIs | Learning Notes

**Status:** Learning — current focus

**Independent assessment:** Not attempted

**Purpose:** Create, list, update and delete ShiftFlow employees and shifts through tested endpoints.

Use this file for guided lessons, notes, my explanations, code examples, questions and evidence. Do not check a skill solely because the code was copied.

## Notes from lessons already started

### GET employee by ID (studied together)
```python
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    employee = load_employee(database_path, employee_id)
    # Handle a missing employee before accessing its methods.
```
**What the code does:** FastAPI maps a GET request such as `/employees/3` to the function; the path value becomes an integer, and `load_employee` looks up that ID in SQLite.

**My explanation:** TODO — Rewrite this in my own words after reviewing.

### Missing employee and 404 (studied together; test still in progress)
```python
from fastapi import FastAPI, HTTPException

if employee is None:
    raise HTTPException(status_code=404, detail="Employee not found")
```
**What the code does:** If the database returns `None`, stop the endpoint and send HTTP 404 instead of calling an Employee method on `None`.

**My explanation:** TODO — Explain why the check must happen before `employee.get_name()`.

**Current test exercise:** Request `/employees/99` in a test database where that ID is absent; assert status code 404 and the error detail. **Not yet recorded as passing.**

---

## Topic-by-topic learning checklist

### 1. Client/server, HTTP and JSON
- [x] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 2. GET and path parameters
- [x] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 3. 404 and other status codes
- [x] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 4. POST and request bodies
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 5. PUT/PATCH updates
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 6. DELETE operations
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 7. Pydantic validation and 422
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 8. Query parameters and list endpoints
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 9. CRUD with SQLite and conflict checks
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 10. Calling external APIs with httpx
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

### 11. API tests with TestClient
- [ ] Learned / discussed
- [ ] Explained in my own words
- [ ] Practiced in ShiftFlow

**My explanation (fill in after the lesson):**

> TODO: Explain this in my own words, including why it matters.

**Code example / file and line:**

```python
# TODO: Add the code I wrote or a short example from ShiftFlow.
```

**What happens step by step:**

1. TODO
2. TODO

**Tests / evidence:** TODO

**Questions or mistakes I learned from:** TODO

## Module learning review
- [ ] I can explain each checked topic in my own words.
- [ ] I have working ShiftFlow examples and test evidence.
- [ ] I can explain mistakes and how I fixed them.
- [ ] Ready for a separate independent challenge (ask for assessment).

**Review date:** TODO
**Relevant commits / PRs:** TODO
**Questions to revisit:** TODO
