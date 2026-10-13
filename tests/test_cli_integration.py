import shiftflow
from employee import Employee


def test_add_employee_creates_object(monkeypatch):
    monkeypatch.setattr(shiftflow, "employees", [])

    answers = iter(["Alex", "Crew"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    shiftflow.add_employee()

    assert len(shiftflow.employees) == 1
    assert isinstance(shiftflow.employees[0], Employee)
    assert shiftflow.employees[0].get_name() == "Alex"
    assert shiftflow.employees[0].get_role() == "Crew"