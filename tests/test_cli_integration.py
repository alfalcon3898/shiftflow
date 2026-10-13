import shiftflow
import pytest
from employee import Employee
from schedule import Schedule
from database import load_employee, load_availability,initialize_database,save_employee,load_all_employees



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

@pytest.fixture
def scheduling_setup(tmp_path, monkeypatch):
    # Use a temporary database so tests never modify real employee data.
    database_path = str(tmp_path / "schedule_test.db")
    initialize_database(database_path)

    # Reset CLI state for each test.
    monkeypatch.setattr(shiftflow, "DATABASE_PATH", database_path)
    monkeypatch.setattr(shiftflow, "employees", [])
    monkeypatch.setattr(shiftflow, "employee_ids", {})
    monkeypatch.setattr(shiftflow, "schedule", Schedule())

    # Create an employee with Tuesday availability.
    employee = Employee("Jordan", "crew")
    employee.add_availability(
        "Tuesday", ("09:00 AM", "05:00 PM")
    )

    employee_id = save_employee(database_path, employee)

    # Persist availability through the CLI's existing database helper.
    from database import replace_employee_availability

    replace_employee_availability(
        database_path, employee_id, employee
    )

    shiftflow.employees.append(employee)
    shiftflow.employee_ids[employee] = employee_id

    return database_path, employee


def test_create_shift_persists(scheduling_setup, monkeypatch, capsys):
    database_path, employee = scheduling_setup

    answers = iter([
        "Jordan",
        "2026-10-13",  # Tuesday
        "09:00 AM",
        "05:00 PM",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.create_shift()

    output = capsys.readouterr().out
    assert "Shift added for Jordan" in output
    assert len(shiftflow.schedule.get_shifts()) == 1

    # Confirm SQLite contains the shift.
    import sqlite3

    with sqlite3.connect(database_path) as connection:
        rows = connection.execute(
            "SELECT date, start_time, end_time FROM shifts"
        ).fetchall()

    assert rows == [
        ("2026-10-13", "09:00 AM", "05:00 PM")
    ]


def test_duplicate_shift_rejected(scheduling_setup, monkeypatch, capsys):
    answers = iter([
        "Jordan", "2026-10-13", "09:00 AM", "05:00 PM",
        "Jordan", "2026-10-13", "09:00 AM", "05:00 PM",
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.create_shift()
    shiftflow.create_shift()

    output = capsys.readouterr().out

    assert "Shift added for Jordan" in output
    assert "Shift rejected:" in output
    assert len(shiftflow.schedule.get_shifts()) == 1


def test_shift_survives_reload(scheduling_setup, monkeypatch):
    answers = iter([
        "Jordan", "2026-10-13", "09:00 AM", "05:00 PM"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.create_shift()

    # Simulate restarting by loading new Employee objects.
    database_path, _ = scheduling_setup
    saved_employees = load_all_employees(database_path)

    shiftflow.employees.clear()
    shiftflow.employee_ids.clear()

    for employee_id, employee in saved_employees:
        shiftflow.employees.append(employee)
        shiftflow.employee_ids[employee] = employee_id

    restored_schedule = shiftflow.load_saved_schedule()
    restored_shifts = restored_schedule.get_shifts()

    assert len(restored_shifts) == 1
    assert restored_shifts[0].get_employee().get_name() == "Jordan"
    assert restored_shifts[0].get_date() == "2026-10-13"
    assert restored_shifts[0].calculate_shift_hr() == 8.0
