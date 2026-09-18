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

def test_raise_error_removing_shift_from_empty_list():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule()
    with pytest.raises(ValueError):
        schedule.remove_shift(shift)
def test_removing_a_shift_that_is_not_added_to_schedule():
    emp = Employee("Allen", "SL")
    shift_a = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    shift_b = Shift(emp, "2026-09-18", "9:00 AM", "6:00 PM")
    schedule = Schedule()
    schedule.add_shift(shift_a)
    with pytest.raises(ValueError):
        schedule.remove_shift(shift_b)
    assert shift_a in schedule.get_shifts()

def test_schedule_integration():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule()
    schedule.add_shift(shift)
    assert shift in schedule.get_shifts()
    stored_shift = schedule.get_shifts()[0]
    assert stored_shift.get_date() == "2026-09-17"
