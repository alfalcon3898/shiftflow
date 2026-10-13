import shiftflow
from employee import Employee


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