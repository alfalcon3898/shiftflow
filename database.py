import sqlite3
from employee import Employee
def initialize_database(database_path):
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
   
    # CREATE employees table
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL )                  
    """)
    
    # CREATE availability table
    cursor.execute("""CREATE TABLE IF NOT EXISTS availability(
        id INTEGER PRIMARY KEY,
        employee_id INTEGER NOT NULL,
        day TEXT NOT NULL,
        start_time TEXT,
        end_time TEXT,
        all_day INTEGER NOT NULL,
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE )                  
        """)
    connection.close()

def save_employee(database_path,employee):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employees(name, role) VALUES(?,?)",
                   (employee.get_name(), employee.get_role())
    )
    employee_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return employee_id

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

def save_availability(database_path, employee_id, employee):
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
    availability = employee.get_availability()
    for day, time_blocks in availability.items():
        #Employee is available all day
        if time_blocks == "ALL_DAY":
            cursor.execute(
            "INSERT INTO availability (employee_id, day, start_time, end_time, all_day) VALUES (?,?,?,?,?)",
            (employee_id, day, None, None, 1)
            )
        else: 
            for time in time_blocks:
                start_time = time[0]
                end_time = time[1]
                cursor.execute("INSERT INTO availability(employee_id, day, start_time, end_time, all_day) VALUES(?,?,?,?,?)",
                           (employee_id, day, start_time, end_time,0)
    )
    connection.commit()
    connection.close()

def load_availability(database_path, employee_id, employee):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT day, start_time, end_time, all_day FROM availability WHERE employee_id = ?",
            (employee_id,)
    )
    results= cursor.fetchall()
    connection.close()
    for day,start_time, end_time, all_day in results:
        if all_day == 1:
            employee.set_all_day_availability(day)
        else:
            employee.add_availability(day, (start_time, end_time))

