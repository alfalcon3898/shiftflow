import pytest
from employee import Employee
from shift import Shift
from schedule import Schedule
import warnings
import random
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

def test_required_staffing_by_sales():
    schedule = Schedule()
    assert schedule.get_required_staffing(5000) == 5

def test_required_staffing_by_sales_2():
    schedule = Schedule()
    assert schedule.get_required_staffing(5001) == 6

def test_staffing_shortage():
    schedule = Schedule()
    required = 6
    current = 3
    assert schedule.get_staffing_shortage(required,current) == 3

def test_staffing_shortage_0():
    schedule = Schedule()
    required = 5
    current = 7
    assert schedule.get_staffing_shortage(required, current) == 0

def test_staffing_shortage_uqual():
    schedule = Schedule()
    required = 5
    current = 5
    assert schedule.get_staffing_shortage(required, current) == 0

def test_get_employee_hrs():
    schedule = Schedule()
    allen = Employee("Allen", "crew")
    bob = Employee("Bob", "crew")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "5:00 AM")
    bob_shift_1 = Shift(bob,"2026-09-23", "11:00 PM", "5:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(bob_shift_1)
    assert schedule.get_employee_hours(allen) == 14

def test_cannot_assign_shift_over_40_hrs():
    schedule = Schedule()
    allen = Employee("allen", "crew")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    allen_shift_3 = Shift(allen, "2026-09-23", "11:00 PM", "7:00 AM")
    allen_shift_4 = Shift(allen, "2026-09-24", "11:00 PM", "9:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(allen_shift_3)
    schedule.add_shift(allen_shift_4)
    proposed_shift = Shift(allen, "2026-09-25", "11:00 PM", "7:00 AM")
    assert schedule.can_assign_shift(allen,proposed_shift ) == False

def test_can_assign_shift_40_hrs():
    schedule = Schedule()
    allen = Employee("allen", "crew")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    allen_shift_3 = Shift(allen, "2026-09-23", "11:00 PM", "7:00 AM")
    allen_shift_4 = Shift(allen, "2026-09-24", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(allen_shift_3)
    schedule.add_shift(allen_shift_4)
    proposed_shift = Shift(allen, "2026-09-25", "11:00 PM", "7:00 AM")
    assert schedule.can_assign_shift(allen,proposed_shift ) == True

def test_remaining_hrs_below_preffered_weekly_targer_hrs():
    schedule = Schedule()
    allen = Employee("allen", "crew", 20)
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "3:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    assert schedule.get_remaining_target_hours(allen) == 8

def test_remaining_hrs_above_preffered_weekly_targer_hrs():
    schedule = Schedule()
    allen = Employee("allen", "crew", 20)
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    allen_shift_3 = Shift(allen, "2026-09-23", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(allen_shift_3)
    assert schedule.get_remaining_target_hours(allen) == 0

def test_chosing_who_get_hrs():
    schedule = Schedule()
    allen = Employee("Allen", "crew", 20, "2021-06-15")
    bob = Employee("Bob", "crew", 20, "2023-06-15")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "5:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "5:00 AM")
    bob_shift_1 = Shift(bob, "2026-09-21", "11:00 PM", "7:00 AM")
    bob_shift_2 = Shift(bob, "2026-09-22", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(bob_shift_1)
    schedule.add_shift(bob_shift_2)
    assert schedule.choose_employee_for_hours(allen, bob) == allen

def test_chosing_who_get_hrs_employee1_has_less():
    schedule = Schedule()
    allen = Employee("Allen", "crew", 20, "2021-06-15")
    bob = Employee("Bob", "crew", 20, "2023-06-15")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    bob_shift_1 = Shift(bob, "2026-09-21", "11:00 PM", "5:00 AM")
    bob_shift_2 = Shift(bob, "2026-09-22", "11:00 PM", "5:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(bob_shift_1)
    schedule.add_shift(bob_shift_2)
    assert schedule.choose_employee_for_hours(allen, bob) == bob

def test_equal_remaining_hrs_use_seniority():
    schedule = Schedule()
    allen = Employee("Allen", "crew", 20, "2021-06-15")
    bob = Employee("Bob", "crew", 20, "2023-06-15")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    bob_shift_1 = Shift(bob, "2026-09-21", "11:00 PM", "7:00 AM")
    bob_shift_2 = Shift(bob, "2026-09-22", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(bob_shift_1)
    schedule.add_shift(bob_shift_2)
    assert schedule.choose_employee_for_hours(allen, bob) == allen

def test_equal_remaining_hrs_use_seniority_employee1_is_not_seniorty():
    schedule = Schedule()
    allen = Employee("Allen", "crew", 20, "2023-06-15")
    bob = Employee("Bob", "crew", 20, "2021-06-15")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    bob_shift_1 = Shift(bob, "2026-09-21", "11:00 PM", "7:00 AM")
    bob_shift_2 = Shift(bob, "2026-09-22", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(bob_shift_1)
    schedule.add_shift(bob_shift_2)
    assert schedule.choose_employee_for_hours(allen, bob) == bob

    
def test_equal_remaining_hrs_and_seniority_random_pick():
    schedule = Schedule()
    allen = Employee("Allen", "crew", 20, "2023-06-15")
    bob = Employee("Bob", "crew", 20, "2023-06-15")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    bob_shift_1 = Shift(bob, "2026-09-21", "11:00 PM", "7:00 AM")
    bob_shift_2 = Shift(bob, "2026-09-22", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(bob_shift_1)
    schedule.add_shift(bob_shift_2)
    result = schedule.choose_employee_for_hours(allen, bob)
    assert result in [allen, bob]

def test_emploee_hours_only_count_selected_week():
    schedule = Schedule()
    allen = Employee("Allen", "crew")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    allen_shift_3 = Shift(allen, "2026-09-28", "11:00 PM", "7:00 AM")
    allen_shift_4 = Shift(allen, "2026-09-29", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(allen_shift_3)
    schedule.add_shift(allen_shift_4)
    assert schedule.get_employee_hours(allen, "2026-09-28") == 16

def test_cannot_pick_up_shift_over_40_hours():
    schedule = Schedule()
    allen = Employee("Allen", "crew")
    bob = Employee("bob", "crew")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    allen_shift_3 = Shift(allen, "2026-09-24", "11:00 PM", "7:00 AM")
    allen_shift_4 = Shift(allen, "2026-09-25", "11:00 PM", "11:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(allen_shift_3)
    schedule.add_shift(allen_shift_4)
    bob_shift_1 = Shift(bob, "2026-09-23", "11:00 PM", "7:00 AM")
    schedule.add_shift(bob_shift_1)
    assert schedule.can_pick_up_shift(allen, bob_shift_1) == False
    assert bob_shift_1.get_employee() == bob
    
def test_can_pick_up_shift_not_over_40_hours():
    schedule = Schedule()
    allen = Employee("Allen", "crew")
    bob = Employee("bob", "crew")
    allen_shift_1 = Shift(allen, "2026-09-21", "11:00 PM", "7:00 AM")
    allen_shift_2 = Shift(allen, "2026-09-22", "11:00 PM", "7:00 AM")
    allen_shift_3 = Shift(allen, "2026-09-24", "11:00 PM", "7:00 AM")
    allen_shift_4 = Shift(allen, "2026-09-25", "11:00 PM", "7:00 AM")
    schedule.add_shift(allen_shift_1)
    schedule.add_shift(allen_shift_2)
    schedule.add_shift(allen_shift_3)
    schedule.add_shift(allen_shift_4)
    bob_shift_1 = Shift(bob, "2026-09-23", "11:00 PM", "7:00 AM")
    schedule.add_shift(bob_shift_1)
    assert schedule.can_pick_up_shift(allen, bob_shift_1) == True
    assert bob_shift_1.get_employee() == allen


