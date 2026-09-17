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

