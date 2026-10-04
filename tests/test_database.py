from database import initialize_database,save_employee
from employee import Employee
import sqlite3
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