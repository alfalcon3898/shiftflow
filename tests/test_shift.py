import pytest
import datetime
from shift import Shift
from employee import Employee


def test_shift_rejects_invalid_date():
    emp = Employee("Allen", "SL")
    with pytest.raises(ValueError):
        Shift(emp, "2026-02-30", "9:00 AM", "5:00 PM")
def test_shift_rejects_invalid_start_time():
    emp = Employee("Allen", "SL")
    with pytest.raises(ValueError):
        Shift(emp,"2026-09-17", "hello", "5:00 PM")
def test_shift_rejects_invalid_end_time():
    emp = Employee("Allen", "SL")
    with pytest.raises(ValueError):
        Shift(emp,"2026-09-17", "9:00 AM", "Hello")

def test_shift_set_date_rejects_invalid_data():
    emp = Employee("Allen","SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:00 PM")
    with pytest.raises(ValueError):
        shift.set_date("2026-02-30")
    assert shift.get_date() == "2026-09-17"
def test_shift_set_start_time_rejects_invalid_time():
    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:00 PM")
    with pytest.raises(ValueError):
        shift.set_start_time("Hello")
    assert shift.get_start_time() == "9:00 AM"

def test_shift_set_end_time_rejects_invalid_time():
    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:00 PM")
    with pytest.raises(ValueError):
        shift.set_end_time("Hello")
    assert shift.get_end_time() == "5:00 PM"

def test_shift_calculate_daytime_hrs():
    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:00 PM")
    assert shift.calculate_shift_hr() == 8.0

def test_shift_calculate_overnight_time_hrs():
    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "11:00 PM", "7:00 AM")
    assert shift.calculate_shift_hr() == 8.0

def test_shift_calculate_fractional_hrs():
    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:30 PM")
    assert shift.calculate_shift_hr() == 8.5

def test_shift_rejects_invalid_employee():
    emp = "Allen"
    with pytest.raises(TypeError):
         Shift(emp,"2026-09-17", "9:00 AM", "5:30 PM")

def test_shift_set_valid_date():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-16", "9:00 AM", "5:00 PM")
    shift.set_date("2026-09-17")
    assert shift.get_date() == "2026-09-17"

def test_shift_set_valid_start_time():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-16", "9:00 AM", "5:00 PM")
    shift.set_start_time("8:00 AM")
    assert shift.get_start_time() == "8:00 AM"

def test_shift_set_valid_end_time():
    emp = Employee("Allen", "SL")
    shift = Shift(emp, "2026-09-16", "9:00 AM", "5:00 PM")
    shift.set_end_time("6:00 PM")
    assert shift.get_end_time() == "6:00 PM"

def test_overlapping_shift():
    emp = Employee("Allen", "SL")
    shift_A = Shift(emp,"2026-09-16", "9:00 AM", "5:00 PM")
    shift_B = Shift(emp,"2026-09-16", "10:00 AM", "6:00 PM")
    assert shift_A.conflicts_with(shift_B) is True

def test_no_overlapping_shift_with_gap():
    emp = Employee("Allen", "SL")
    shift_A = Shift(emp,"2026-09-16", "9:00 AM", "3:00 PM")
    shift_B = Shift(emp,"2026-09-16", "4:00 PM", "6:00 PM")
    assert shift_A.conflicts_with(shift_B) is False

def test_overlaping_but_diffrent_employee():
    emp_A = Employee("Allen", "SL")
    emp_B = Employee("Terry", "SL")
    shift_A = Shift(emp_B,"2026-09-16", "9:00 AM", "5:00 PM")
    shift_B = Shift(emp_A,"2026-09-16", "10:00 AM", "6:00 PM")
    assert shift_A.conflicts_with(shift_B) is False
   

def test_no_overlapping_but_shift_are_back_to_back():
     emp = Employee("Allen", "SL")
     shift_A = Shift(emp,"2026-09-16", "9:00 AM", "12:00 PM")
     shift_B = Shift(emp,"2026-09-16", "12:00 PM", "5:00 PM")
     assert shift_A.conflicts_with(shift_B) is False

def test_shift_crossing_midnight_overlap_conflict():
    emp = Employee("Allen", "SL")
    shift_A = Shift(emp,"2026-09-16", "11:00 PM", "7:00 AM")
    shift_B = Shift(emp,"2026-09-17", "6:00 AM", "2:00 PM")
    assert shift_A.conflicts_with(shift_B) is True

def test_set_employee():
    allen = Employee("Allen", "crew")
    bob = Employee("Bob", "crew")
    shift_A = Shift(allen,"2026-09-16", "11:00 PM", "7:00 AM")
    shift_A.set_employee(bob)
    assert shift_A.get_employee() == bob
