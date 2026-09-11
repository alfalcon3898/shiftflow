import pytest
from employee import Employee


def test_creates_employee_with_valid_data():
    emp = Employee("Allen" , "SL")
    assert emp.get_name() == "Allen"

def test_get_role_returns_correct_role():
    emp = Employee("Allen", "SL")
    assert emp.get_role() == "SL"

def test_new_employee_has_empty_availability():
    emp = Employee("Allen", "SL")
    assert emp.get_availability() == []

def test_empty_name_raise_error():
    with pytest.raises(ValueError):
        Employee("", "SL")

def test_long_name_raise_error():
    with pytest.raises(ValueError):
        Employee("a" * 101,"SL")

def test_empty_role_raise_error():
    with pytest.raises(ValueError):
        Employee("Allen", "")

def test_long_role_raise_error():
    with pytest.raises(ValueError):
        Employee("Allen" , "a" * 51)

def test_add_availability():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday, 4-11PM")
    assert emp.get_availability() == ["Monday, 4-11PM"]
   