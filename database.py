import sqlite3
from employee import Employee
def initialize_database(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL )                  
    """)
    connection.close()

def save_employee(database_path,employee):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employees(name, role) VALUES(?,?)",
                   (employee.get_name(), employee.get_role())
    )
    connection.commit()
    connection.close()

def load_employee(database_path, employee_id):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, role FROM employees WHERE id = ?",
        (employee_id,)
    )
    result = cursor.fetchone()
    connection.close()
    return Employee(result[0], result[1])
