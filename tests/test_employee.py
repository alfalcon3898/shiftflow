import pytest
from employee import Employee
from employee import AvailabilityStatus


def test_creates_employee_with_valid_data():
    emp = Employee("Allen" , "SL")
    assert emp.get_name() == "Allen"

def test_get_role_returns_correct_role():
    emp = Employee("Allen", "SL")
    assert emp.get_role() == "SL"

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
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    assert emp.get_availability() == {
    "Monday": [("4:00 PM", "11:00 PM")]
}
   
def test_remove_availability():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    emp.remove_availability("Monday", ("4:00 PM", "11:00 PM"))
    assert emp.get_availability() == {}

def test_remove_availabilty_raise_not_found_error():
    with pytest.raises(ValueError):
        emp = Employee("Allen","SL")
        emp.remove_availability("Monday", ("4:00 PM", "11:00 PM"))

def test_clear_availability():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    emp.add_availability("Tuesday", ("4:00 PM", "11:00 PM"))
    emp.add_availability("Thursday", ("4:00 PM", "11:00 PM"))
    emp.clear_availability()
    assert emp.get_availability() == {}
    
def test_corrupted_v1_is_rejected():
    with pytest.raises(ValueError):
        Employee("& C:/Users/alnig/AppData/Local/Programs/Python/Python314/python.exe c:/Users/alnig/Documents/shiftflow/shiftflow.py","SL")

def test_get_availability_returns_copy():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday",("4:00 PM", "11:00 PM"))

    availability = emp.get_availability()
    availability.clear()

    assert emp.get_availability() == {
        "Monday": [("4:00 PM", "11:00 PM")]
    }
    availability = emp.get_availability()
    availability["Monday"].append(("9:00 AM", "12:00 PM"))
    assert emp.get_availability() == {
        "Monday": [("4:00 PM", "11:00 PM")]
    }

def test_availability_status_values():
    assert AvailabilityStatus.AVAILABLE.value == "available to work" 
    assert AvailabilityStatus.UNAVAILABLE.value == "unavailable to work" 
    assert AvailabilityStatus.UNKNOWN.value == "availability not entered"

def test_new_employee_has_empty_availability():
    emp = Employee("Allen", "SL")
    assert emp.get_availability() == {}    

def test_check_availability_wiithin_block():
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))

    result = emp.check_availability("Monday", ("9:00 AM", "12:00 PM"))

    assert result == AvailabilityStatus.AVAILABLE

def test_check_unvailability_wiithin_block():
    emp = Employee("Allen","SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    result = emp.check_availability("Monday", ("11:00 AM", "3:00 PM"))

    assert result == AvailabilityStatus.UNAVAILABLE

def test_check_unknown_wiithin_block():
    emp = Employee("Allen", "SL")
    result = emp.check_availability("Monday", ("11:00 AM", "3:00 PM"))
    assert result == AvailabilityStatus.UNKNOWN


def test_check_availability_wiithin_block_multiple_checks():
    emp = Employee("Allen","SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    emp.add_availability("Monday", ("2:00 PM", "6:00 PM"))
    result = emp.check_availability("Monday", ("3:00 PM", "5:00 PM"))

    assert result == AvailabilityStatus.AVAILABLE

def test_setting_availability_all_day():
    emp = Employee("Allen","SL")
    emp.set_all_day_availability("Monday")
    result = emp.check_availability("Monday", ("3:00 PM", "5:00 PM"))
    assert result == AvailabilityStatus.AVAILABLE

def test_add_availability_rejects_invalid_time():
    emp = Employee("Allen", "SL")
    with pytest.raises(ValueError):
        emp.add_availability("Monday", ("banana", "12:00 PM"))
    assert emp.get_availability() == {}

def test_employee_object_being_created_with_defult_40_hrs():
    emp = Employee("Allen","SL")
    assert emp.get_target_weekly_hr() == 40

def test_employee_can_have_custom_target_weekly_hours():
    emp = Employee("Allen","SL", 20)
    assert emp.get_target_weekly_hr() == 20
    
def test_target_weekly_hrs_cannot_exceed_40():
    with pytest.raises(ValueError):
        Employee("Allen", "SL", 41) 

def test_target_weekly_hrs_cannot_be_less_than_0():
    with pytest.raises(ValueError):
        Employee("Allen", "SL", -1)

def test_add_hire_date():
    emp = Employee("Allen", "crew", 20, "2021-06-15")
    assert emp.get_hire_date() == "2021-06-15"

def test_invalid_data_hire():
    with pytest.raises(ValueError):
        Employee("Allen", "crew", 20, "banana")

def test_none_data_hire():
    emp = Employee("Allen", "crew", 20,)
    assert emp.get_hire_date() is None