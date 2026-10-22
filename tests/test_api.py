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
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)
    app = create_app(database_path)

    #send a request 
    with TestClient(app) as client:
        response = client.get("/employees/999")
    assert response.status_code == 404
    assert response.json() == {"detail":"Employee not found"}

def test_get_employee_invalid_id(tmp_path):
    database_path = tmp_path /"test_shift.db"
    initialize_database(database_path)
    app = create_app(database_path)
    #send request
    with TestClient(app) as client:
        response = client.get("/employees/banana")
    assert response.status_code == 422
    
