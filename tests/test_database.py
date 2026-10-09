from database import initialize_database,save_employee, load_employee, save_availability, load_availability, save_shift, load_shifts,load_shift
from employee import Employee
from shift import Shift
import sqlite3
import pytest
from database import load_shift
def test_initialize_database_employee_table(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';")
    result = cursor.fetchone()
    assert result == ('employees',)
    connection.close()

def test_save_employee(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)
    employee = Employee("Allen","SL")
    save_employee(database_path,employee)
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name, role FROM employees WHERE name='Allen';")
    result = cursor.fetchone()
    assert result == ("Allen","SL")
    connection.close()

def test_load_employee(tmp_path):
    database_path = tmp_path/"test_shiftflow.db"
    initialize_database(database_path)
    
    employee = Employee("Allen","SL")
    save_employee(database_path, employee)

    loaded_employee = load_employee(database_path,1)
    assert loaded_employee.get_name() == "Allen"
    assert loaded_employee.get_role() == "SL"

def test_initialize_database_availability_table(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='availability';")
    results = cursor.fetchone()
    assert results == ('availability',)
    connection.close()

def test_availability_reject_unknown_employee(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
    with pytest.raises(sqlite3.IntegrityError):
        cursor.execute(
            "INSERT INTO availability (employee_id, day, all_day) VALUES (?, ?, ?)",
            (999, "Monday", 1)
    )

def test_save_availability(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)
    
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
    
    emp = Employee("Allen","SL")
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    employee_id  = save_employee(database_path, emp)
    assert isinstance(employee_id, int)
    save_availability(database_path, employee_id, emp)

    cursor.execute(
        "SELECT employee_id, day, start_time, end_time, all_day FROM availability WHERE employee_id = ?",
        (employee_id,)
    )
    result = cursor.fetchone()
    assert result == (employee_id, "Monday", "4:00 PM", "11:00 PM",0)
    connection.close()

def test_save_availability_all_day(tmp_path):
    database_path = tmp_path/"test_shiftflow.db"
    initialize_database(database_path)

    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    emp = Employee("Allen", "SL")
    emp.set_all_day_availability("Tuesday")
    employee_id  = save_employee(database_path, emp)
    assert isinstance(employee_id, int)
    save_availability(database_path, employee_id, emp)
    cursor.execute(
            "SELECT employee_id, day, start_time, end_time, all_day FROM availability WHERE employee_id = ?",
            (employee_id,)
        )
    result = cursor.fetchone()
    assert result == (employee_id, "Tuesday",None, None,1)
    connection.close()

def test_save_multiple_availability_blocks(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)
        
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
        
    emp = Employee("Allen","SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    employee_id  = save_employee(database_path, emp)
    assert isinstance(employee_id, int)
    save_availability(database_path, employee_id, emp)
    
    cursor.execute(
         "SELECT employee_id, day, start_time, end_time, all_day FROM availability WHERE employee_id = ? ORDER BY id",
            (employee_id,)
        )
    results = cursor.fetchall()

    assert results == [
     (employee_id, "Monday", "9:00 AM", "12:00 PM",0), 
     (employee_id, "Monday", "4:00 PM", "11:00 PM",0)
    ]
    connection.close()

def test_load_availability(tmp_path):
    database_path = tmp_path/"test_shiftflow.db"
    initialize_database(database_path)
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    employee_id  = save_employee(database_path, emp)
    assert isinstance(employee_id, int)
    save_availability(database_path, employee_id, emp)
    loaded_employee = load_employee(database_path, employee_id)
    load_availability(database_path, employee_id, loaded_employee)
    assert loaded_employee.get_availability() == {
    "Monday": [("4:00 PM", "11:00 PM")]
}

def test_load_availability_multiple_time_and_all_day(tmp_path):
    database_path = tmp_path/"test_shiftflow.db"
    initialize_database(database_path)
    emp = Employee("Allen", "SL")
    emp.add_availability("Monday", ("9:00 AM", "12:00 PM"))
    emp.add_availability("Monday", ("4:00 PM", "11:00 PM"))
    emp.set_all_day_availability("Tuesday")
    employee_id  = save_employee(database_path, emp)
    assert isinstance(employee_id, int)
    save_availability(database_path, employee_id, emp)
    loaded_employee = load_employee(database_path, employee_id)
    load_availability(database_path, employee_id, loaded_employee)
    assert loaded_employee.get_availability() == {
    "Monday": [
        ("9:00 AM", "12:00 PM"),
        ("4:00 PM", "11:00 PM")
               ],
    "Tuesday": "ALL_DAY"
    
}

def test_initialize_database_shifts_table(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name ='shifts';")
    results = cursor.fetchone()
    assert results == ('shifts',)
    connection.close()


def test_save_shift(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()


    emp = Employee("Allen", "SL")
    shift = Shift(emp,"2026-09-17", "9:00 AM", "5:00 PM")
    employee_id = save_employee(database_path, emp)
    assert isinstance(employee_id, int)
    save_shift(database_path, employee_id, shift)
    
    cursor.execute(
        "SELECT employee_id, date, start_time, end_time FROM shifts WHERE employee_id = ?  ORDER BY id",
        (employee_id,)
    )
    result = cursor.fetchone()
    assert result == (employee_id, "2026-09-17", "9:00 AM", "5:00 PM")
    connection.close()
    


def test_load_shift(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)

    emp = Employee("Allen", "SL")
    employee_id = save_employee(database_path, emp)

    shift = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    save_shift(database_path, employee_id, shift)
    loaded_shift = load_shift(database_path, employee_id)
    assert isinstance(loaded_shift, Shift)
    assert loaded_shift.get_date() == "2026-09-17"
    assert loaded_shift.get_start_time() == "9:00 AM"
    assert loaded_shift.get_end_time() =="5:00 PM"
    assert loaded_shift.get_employee().get_name() == "Allen"

def test_load_multiple_shifts(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)

    emp = Employee("Allen", "SL")
    employee_id = save_employee(database_path, emp)

    shift1 = Shift(emp, "2026-09-17", "9:00 AM", "5:00 PM")
    shift2 = Shift(emp, "2026-09-18", "10:00 AM", "6:00 PM")
    save_shift(database_path, employee_id, shift1)
    save_shift(database_path, employee_id, shift2)
    loaded_shifts = load_shifts(database_path, employee_id)
    assert isinstance(loaded_shifts, list)
    assert len(loaded_shifts) == 2
    assert loaded_shifts[0].get_date() == "2026-09-17"
    assert loaded_shifts[1].get_date() == "2026-09-18"


def test_load_nonexistent_employee(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)

    result = load_employee(database_path, 999)

    assert result is None


def test_save_load_employee_extra_fields(tmp_path):
    database_path = tmp_path / "test_shiftflow.db"
    initialize_database(database_path)

    employee = Employee("Allen", "SL", 32, "2024-01-15")
    employee_id = save_employee(database_path, employee)

    loaded_employee = load_employee(database_path, employee_id)

    assert loaded_employee.get_target_weekly_hr() == 32
    assert loaded_employee.get_hire_date() == "2024-01-15"