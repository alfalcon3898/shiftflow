from database import initialize_database,save_employee, load_employee, save_availability
from employee import Employee
import sqlite3
import pytest
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
