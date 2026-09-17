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
        Shift(emp,"2026-9-17", "hello", "5:00 PM")