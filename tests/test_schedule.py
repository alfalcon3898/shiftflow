import pytest
from employee import Employee
from shift import Shift
from schedule import Schedule
import warnings

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

def test_remove_shift_rejects_invalid_type():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule()
    schedule.add_shift(shift)
    with pytest.raises(TypeError):
        schedule.remove_shift("Allen")

def test_add_shift_rejects_duplicate():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    schedule = Schedule()
    schedule.add_shift(shift)
    with pytest.raises(ValueError):
        shift_a = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
        schedule.add_shift(shift_a)
    assert len(schedule.get_shifts()) == 1

def test_add_shift_rejects_after_checking_availability():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    schedule = Schedule()
    shift = Shift(emp, "2026-09-21", "3:00 PM", "5:00 PM")
    with pytest.raises(ValueError):
        schedule.add_shift(shift)
    assert len(schedule.get_shifts()) == 0

def test_add_shift_accepts_available_employee():
    emp = Employee("Allen", "SL")   
    emp.add_availability("Monday",("9:00 AM","12:00 PM"))
    schedule = Schedule()
    shift = Shift(emp, "2026-09-21", "10:00 AM", "12:00 PM")
    schedule.add_shift(shift)
    assert len(schedule.get_shifts()) == 1

def test_add_shift_when_Availabilty_Uknown():
    emp = Employee("Allen","SL")
    schedule = Schedule()
    shift = Shift(emp, "2026-09-21", "10:00 AM", "12:00 PM")
    with pytest.warns(UserWarning):
        schedule.add_shift(shift)
    assert len(schedule.get_shifts()) == 1

def test_add_shift_availabilty_set_all_day():
    emp = Employee("Allen", "SL")   
    emp.set_all_day_availability("Monday")
    schedule = Schedule()
    shift = Shift(emp, "2026-09-21", "10:00 AM", "12:00 PM")
    schedule.add_shift(shift)
    assert len(schedule.get_shifts()) == 1

def test_add_over_night_shift_tet_availabilty():
    emp = Employee("Allen", "SL")   
    emp.add_availability("Monday",("10:00 PM","7:00 AM"))
    schedule = Schedule()
    shift = Shift(emp, "2026-09-21", "11:00 PM", "6:00 AM")
    schedule.add_shift(shift)
    assert len(schedule.get_shifts()) == 1

def test_add_over_night_shift_tet_availabilty_2():
    emp = Employee("Allen", "SL")   
    emp.add_availability("Monday",("10:00 PM","7:00 AM"))
    schedule = Schedule()
    shift = Shift(emp, "2026-09-21", "11:00 PM", "8:00 AM")
    with pytest.raises(ValueError):
        schedule.add_shift(shift)

def test_specific_availability_replaces_all_day():
    emp = Employee("Alle", "SL")
    emp.set_all_day_availability("Monday")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    assert emp.get_availability() == {
        "Monday": [("9:00 AM", "12:00 PM")]
    }
def test_all_day_replaces_specific_availability():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    emp.set_all_day_availability("Monday")
    assert emp.get_availability()["Monday"] == "ALL_DAY"