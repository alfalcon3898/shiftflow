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

**My explanation (reviewed):** We might request different employee IDs, not just 5. The client requests information using GET; FastAPI connects the matching route to my Python function. It gets the employee ID, but it does not already have that employee's information. `load_employee()` retrieves the information from the database.

### Missing employee and 404 (studied and tested)
```python
from fastapi import FastAPI, HTTPException

if employee is None:
    raise HTTPException(status_code=404, detail="Employee not found")
```
**What the code does:** If the database returns `None`, stop the endpoint and send HTTP 404 instead of calling an Employee method on `None`.

**My explanation (reviewed):** `None` means the employee wasn't found. We check it because continuing to call `employee.get_name()` on `None` would cause an error. Instead, we raise an HTTP exception so the API returns 404.

**Test evidence (user-reported 2026-10-27):** `python -m pytest tests/test_api.py -v` — all three tests passed according to the learner. Test for missing `/employees/999` asserts 404 and `{"detail": "Employee not found"}`. The run was not independently observed; code below is from the learner's shared test file.

---

## Topic-by-topic learning checklist

### 1. Client/server, HTTP and JSON
- [x] Learned / discussed
- [x] Explained in my own words
- [x] Practiced in ShiftFlow

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
- [x] Explained in my own words
- [x] Practiced in ShiftFlow

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
- [x] Explained in my own words
- [x] Practiced in ShiftFlow

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
- [x] Learned / discussed (FastAPI path type validation and 422 only; Pydantic request models not yet studied)
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
- [x] Learned / discussed (query parameter concepts only; no list endpoint implemented)
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
- [x] Learned / discussed
- [x] Explained in my own words
- [x] Practiced in ShiftFlow

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

## 2026-10-27 — Reviewed understanding and tested GET employee endpoint

**Status:** Guided learning completed for the GET-by-ID/API-test section. Not an independent mastery assessment.

### My explanations (from conversation, lightly edited for spelling and technical accuracy)
- **Client:** The ShiftFlow website is the client because it requests employee information.
- **HTTP:** GET is an HTTP method for requesting information. The client sends the HTTP request, and the server sends the HTTP response; HTTP is the communication protocol, not a separate sender. This distinction needed extra review.
- **API vs. FastAPI:** An API defines how different applications can request and receive information. FastAPI is the Python framework I use to build endpoints that receive requests and return responses.
- **Path parameters:** We use `{employee_id}` because we might request different employee IDs, not just 5.
- **Query parameters:** `/employees?role=Manager` asks for employees whose role is Manager, potentially more than one employee. This was explained, but filtering has not been implemented yet.
- **Type validation:** `employee_id: int` means FastAPI expects an integer ID. `/employees/banana` produces 422 because it is the wrong input type; FastAPI handles this validation automatically.
- **Database:** FastAPI gets the requested ID, but doesn't already have the employee data. `load_employee()` retrieves it from SQLite.
- **404:** If the employee is `None`, continuing to call `get_name()` would fail. We deliberately raise an `HTTPException` to return 404 instead.
- **Response:** We call methods on the Employee object to retrieve data, put selected fields in a Python dictionary, and FastAPI serializes that dictionary to JSON.
- **TestClient:** It simulates a client making requests to the API, without testing an actual website button.
- **tmp_path:** A separate test database lets us change data and run tests without affecting actual ShiftFlow data.
- **assert:** It checks that the actual response matches what we expect. `status_code` checks HTTP status; `response.json()` checks the returned data or error message.

### My API tests — code shared during the lesson

```python
from fastapi.testclient import TestClient

from employee import Employee
from database import initialize_database, save_employee
from api import create_app


def test_get_employee(tmp_path):
    # Create a separate test database and save a sample employee.
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)

    employee = Employee("Allen", "SL", 20)
    employee_id = save_employee(database_path, employee)

    # Point the API at our test database.
    app = create_app(database_path)

    # Request the saved employee through the API.
    with TestClient(app) as client:
        response = client.get(f"/employees/{employee_id}")

    # Verify the request succeeded and returned the correct employee data.
    assert response.status_code == 200
    assert response.json() == {
        "id": employee_id,
        "name": "Allen",
        "role": "SL",
        "target_weekly_hr": 20,
        "hire_date": None,
        "availability": {}
    }


def test_get_employee_not_found(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)
    app = create_app(database_path)

    # Send a request.
    with TestClient(app) as client:
        response = client.get("/employees/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Employee not found"}


def test_get_employee_invalid_id(tmp_path):
    database_path = tmp_path / "test_shift.db"
    initialize_database(database_path)
    app = create_app(database_path)

    # Send a request.
    with TestClient(app) as client:
        response = client.get("/employees/banana")

    assert response.status_code == 422
```

**Test run:** `python -m pytest tests/test_api.py -v` — learner reports all three tests passed: 200, 404, 422. Not independently verified from terminal output.

**Review later:** HTTP vs. client, API vs. FastAPI, JSON vs. Python dictionary. **Next lesson:** POST requests and request bodies.

---

## Module learning review
- [ ] I can explain each checked topic in my own words.
- [ ] I have working ShiftFlow examples and test evidence.
- [ ] I can explain mistakes and how I fixed them.
- [ ] Ready for a separate independent challenge (ask for assessment).

**Review date:** TODO
**Relevant commits / PRs:** TODO
**Questions to revisit:** TODO
