import shiftflow
from employee import Employee
from database import load_employee, load_availability



def test_add_employee_creates_object(monkeypatch, tmp_path):
    test_database = tmp_path / "test_shiftflow.db"

    monkeypatch.setattr(shiftflow, "DATABASE_PATH", str(test_database))
    monkeypatch.setattr(shiftflow, "employees", [])
    monkeypatch.setattr(shiftflow, "employee_ids", {})

    shiftflow.initialize_database(str(test_database))

    answers = iter(["Alex", "Crew"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.add_employee()

    assert len(shiftflow.employees) == 1
    assert isinstance(shiftflow.employees[0], Employee)
    assert shiftflow.employees[0].get_name() == "Alex"
    assert shiftflow.employees[0].get_role() == "Crew"

    from database import load_employee

    saved_employee = load_employee(str(test_database), 1)

    assert saved_employee is not None
    assert saved_employee.get_name() == "Alex"
    assert saved_employee.get_role() == "Crew"


def test_update_role_persists(monkeypatch, tmp_path):
    db = str(tmp_path / "roles.db")
    shiftflow.initialize_database(db)

    monkeypatch.setattr(shiftflow, "DATABASE_PATH", db)
    monkeypatch.setattr(shiftflow, "employees", [])
    monkeypatch.setattr(shiftflow, "employee_ids", {})

    employee = Employee("Alex", "Crew")
    employee_id = shiftflow.save_employee(db, employee)
    shiftflow.employees.append(employee)
    shiftflow.employee_ids[employee] = employee_id

    answers = iter(["Alex", "SL"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.update_role()

    assert employee.get_role() == "SL"
    assert load_employee(db, employee_id).get_role() == "SL"


def test_delete_employee_persists(monkeypatch, tmp_path):
    db = str(tmp_path / "delete.db")
    shiftflow.initialize_database(db)

    monkeypatch.setattr(shiftflow, "DATABASE_PATH", db)
    monkeypatch.setattr(shiftflow, "employees", [])
    monkeypatch.setattr(shiftflow, "employee_ids", {})

    employee = Employee("Alex", "Crew")
    employee_id = shiftflow.save_employee(db, employee)
    shiftflow.employees.append(employee)
    shiftflow.employee_ids[employee] = employee_id

    monkeypatch.setattr("builtins.input", lambda _: "Alex")

    shiftflow.delete_employee()

    assert shiftflow.employees == []
    assert load_employee(db, employee_id) is None


def test_availability_persists(monkeypatch, tmp_path):
    db = str(tmp_path / "availability.db")
    shiftflow.initialize_database(db)

    monkeypatch.setattr(shiftflow, "DATABASE_PATH", db)
    monkeypatch.setattr(shiftflow, "employees", [])
    monkeypatch.setattr(shiftflow, "employee_ids", {})

    employee = Employee("Alex", "Crew")
    employee_id = shiftflow.save_employee(db, employee)
    shiftflow.employees.append(employee)
    shiftflow.employee_ids[employee] = employee_id

    answers = iter(["Alex", "Monday", "n", "09:00 AM", "05:00 PM"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.update_availability()

    loaded = load_employee(db, employee_id)
    load_availability(db, employee_id, loaded)

    assert loaded.get_availability()["Monday"] == [
        ("09:00 AM", "05:00 PM")
    ]