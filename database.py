import sqlite3
from employee import Employee
from shift import Shift
def initialize_database(database_path):
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()
   
    # CREATE employees table
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    target_weekly_hr INTEGER NOT NULL DEFAULT 40,
    hire_date TEXT)                  
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
   # CREATE shifts table
    cursor.execute("""CREATE TABLE IF NOT EXISTS shifts(
        id INTEGER PRIMARY KEY,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        start_time TEXT NOT NULL,
        end_time TEXT NOT NULL,
        FOREIGN KEY (employee_id)
        REFERENCES employees(id)
        ON DELETE CASCADE )                  
        """)
    connection.close()

def save_employee(database_path,employee):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO employees(name, role, target_weekly_hr, hire_date) VALUES(?,?,?,?)",
                   (employee.get_name(), employee.get_role(),employee.get_target_weekly_hr(),employee.get_hire_date())
    )
    employee_id = cursor.lastrowid
    connection.commit()
    connection.close()
    return employee_id

def load_employee(database_path, employee_id):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT name, role,target_weekly_hr, hire_date FROM employees WHERE id = ?",
        (employee_id,)
    )
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return None
    return Employee(result[0], result[1],result[2], result[3])

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

def save_shift(database_path, employee_id, shift):
    connection = sqlite3.connect(database_path)
    connection.execute("PRAGMA foreign_keys = ON")
    cursor = connection.cursor()

    cursor.execute("INSERT INTO shifts(employee_id, date, start_time, end_time) VALUES(?,?,?,?)",
                           (employee_id, shift.get_date(),shift.get_start_time(),shift.get_end_time())
     )
    connection.commit()
    connection.close()


def load_shift(database_path, employee_id):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT date, start_time, end_time FROM shifts WHERE employee_id = ?  ORDER BY id",
                (employee_id,)
        )
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return None
    return Shift(load_employee(database_path, employee_id),result[0], result[1], result[2])


def load_shifts(database_path, employee_id):
    loaded_shifts = []
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()


    cursor.execute(
        "SELECT date, start_time, end_time FROM shifts WHERE employee_id = ? ORDER BY id",
        (employee_id,)
    )

    results = cursor.fetchall()
    connection.close()
    employee = load_employee(database_path, employee_id)

    for result in results:
        shift = Shift(employee, result[0], result[1], result[2])
        loaded_shifts.append(shift)

    return loaded_shifts

def load_all_employees(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute("SELECT id FROM employees ORDER BY id")
    results = cursor.fetchall()
    connection.close()

    employees = []

    for (employee_id,) in results:
        employee = load_employee(database_path, employee_id)
        load_availability(database_path, employee_id, employee)
        employees.append((employee_id, employee))

    return employees