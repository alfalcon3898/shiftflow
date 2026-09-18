import pytest
from employee import Employee
from shift import Shift
from schedule import Schedule

def test_add_shift():
    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule() 
    schedule.add_shift(shift)
    assert shift in schedule.get_shifts()

def test_add_shift_rejects_invalid_type():
    with pytest.raises(TypeError):
        shift = "Allen"
        schedule = Schedule() 
        schedule.add_shift(shift)

def test_get_shift_empty():
    schedule = Schedule() 
    assert schedule.get_shifts() == []

def test_get_shift_returns_copy():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule()
    schedule.add_shift(shift)
    shifts = schedule.get_shifts()
    shifts.clear()
    assert shift in schedule.get_shifts()

def test_remove_shift():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule()
    schedule.add_shift(shift)
    schedule.remove_shift(shift)
    assert schedule.get_shifts() == []