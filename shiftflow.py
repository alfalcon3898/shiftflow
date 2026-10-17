import sqlite3
from shift import Shift
from schedule import Schedule
from database import save_shift
import json
from datetime import datetime
from employee import Employee
from database import (
    initialize_database,
    save_employee,
    load_all_employees,
    update_employee_role,
    delete_employee_record,
    replace_employee_availability,
)

employees = []
DATABASE_PATH = "shiftflow.db"
employee_ids = {}

# Manage all scheduled shifts through the Schedule class.
schedule = Schedule()

def find_employee(name):
    for employee in employees:
        if employee.get_name().lower() == name.strip().lower():
            return employee
    return None


def display_employee(employee):
    print(f"Name: {employee.get_name()}")
    print(f"Role: {employee.get_role()}")

    availability = employee.get_availability()

    if not availability:
        print("Availability: Not entered")
        return

    print("Availability:")
    for day, blocks in availability.items():
        if blocks == "ALL_DAY":
            print(f"  {day}: All day")
        else:
            for start_time, end_time in blocks:
                print(f"  {day}: {start_time} - {end_time}")

def load_employees():
    global employees

    try:
        with open("employees.json", "r") as file:
            employees = json.load(file)
    except FileNotFoundError:
        employees = []


#save employee
def save_employees():
    with open("employees.json", "w") as file:
        json.dump(employees, file, indent=4)

# Add a new employee to the employees list
def add_employee():
    name = input("Enter employee name: ")
    role = input("Enter employee role: ")

    for existing_employee in employees:
        if existing_employee.get_name().lower() == name.lower():
            print("Employee already added")
            return

    try:
        new_employee = Employee(name, role)
    except ValueError as error:
        print(f"Error: {error}")
        return

    employee_id = save_employee(DATABASE_PATH, new_employee)

    employees.append(new_employee)
    employee_ids[new_employee] = employee_id

    print("Employee added")

# Search for an employee by name
def search_employee():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    display_employee(employee)

# Display all employees and their roles
def view_employees():
    if not employees:
        print("No employees found")
        return

    for employee in sorted(employees, key=lambda e: e.get_name().lower()):
        display_employee(employee)
        print("----------------")
         
#Show only one employee
def view_employee():
    search_employee()
        

# Update an employee's availability
def update_availability():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    # Ask which day the employee is available.
    day = input("Enter day: ").strip().title()

    if not day:
        print("Day cannot be empty")
        return

    # Check whether the employee is available all day.
    choice = input("Available all day? (y/n): ").strip().lower()

    if choice == "y":

        # Check if all-day availability already exists.
        if employee.get_availability().get(day) == "ALL_DAY":
            print("Availability already exists")
            return

        employee.set_all_day_availability(day)

    elif choice == "n":

        # Ask for the start and end times.
        start_time = input("Start time (e.g. 09:00 AM): ").strip()
        end_time = input("End time (e.g. 05:00 PM): ").strip()

        # Check for duplicate availability entries.
        existing = employee.get_availability().get(day, [])

        if existing != "ALL_DAY" and (start_time, end_time) in existing:
            print("Availability already exists")
            return

        try:
            employee.add_availability(day, (start_time, end_time))
        except (ValueError, IndexError) as error:
            print(f"Invalid availability: {error}")
            return

    else:
        print("Please enter y or n")
        return

    # Save the updated availability to SQLite.
    replace_employee_availability(
        DATABASE_PATH,
        employee_ids[employee],
        employee
    )

    print(f"Availability updated for {employee.get_name()}")

# Delete employee
def delete_employee():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    # Remove the employee's shifts from the active schedule
    for shift in schedule.get_shifts().copy():
        if shift.get_employee() is employee:
            schedule.remove_shift(shift)

    # Delete employee from SQLite
    delete_employee_record(DATABASE_PATH, employee_ids[employee])

    # Remove employee from memory
    employees.remove(employee)
    del employee_ids[employee]

    print(f"{employee.get_name()} was deleted.")

# Update employee update role
def update_role():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    new_role = input("Enter new employee role: ")

    try:
        employee.set_role(new_role)
    except ValueError as error:
        print(f"Invalid role: {error}")
        return

    update_employee_role(
        DATABASE_PATH, employee_ids[employee], employee.get_role()
    )
    print(f"{employee.get_name()} role updated to {employee.get_role()}")

#remove availabailty 
def remove_availability():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    day = input("Enter day: ").strip().title()
    availability = employee.get_availability()

    if day not in availability:
        print("No availability for that day")
        return

    if availability[day] == "ALL_DAY":
        print("To remove all-day availability, use Clear Availability.")
        return

    start_time = input("Start time to remove: ").strip()
    end_time = input("End time to remove: ").strip()

    try:
        employee.remove_availability(day, (start_time, end_time))
    except ValueError as error:
        print(f"Error: {error}")
        return

    replace_employee_availability(
        DATABASE_PATH, employee_ids[employee], employee
    )
    print(f"Availability removed from {employee.get_name()}")


def employee_count():
    print(f"Total Employees: {len(employees)}")


def clear_availability():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    employee.clear_availability()

    replace_employee_availability(
        DATABASE_PATH, employee_ids[employee], employee
    )
    print(f"{employee.get_name()}'s availability was cleared.")

#Number of employee with certain role
def number_role_types():
    counts = {"crew": 0, "kl": 0, "sl": 0}

    for employee in employees:
        role = employee.get_role().lower()
        if role in counts:
            counts[role] += 1

    print("-----Roles-----")
    print(f"Crew: {counts['crew']}")
    print(f"KL: {counts['kl']}")
    print(f"SL: {counts['sl']}")
    print(f"Number of employees: {len(employees)}")

  # Create and assign a new employee shift
def create_shift():
    name = input("Enter employee name: ")
    employee = find_employee(name)

    if employee is None:
        print("Employee not found")
        return

    # Collect the date and times for the proposed shift.
    date = input("Shift date (YYYY-MM-DD): ").strip()
    start_time = input("Start time (e.g. 09:00 AM): ").strip()
    end_time = input("End time (e.g. 05:00 PM): ").strip()

    try:
        # Create a Shift object using the existing Employee object.
        shift = Shift(employee, date, start_time, end_time)

        # Check the employee's 40-hour weekly limit.
        if not schedule.can_assign_shift(employee, shift):
            print("Shift rejected: employee would exceed 40 weekly hours.")
            return

        # Check availability and overlapping shifts.
        schedule.add_shift(shift)

        try:
            # Save the validated shift to SQLite.
            save_shift(DATABASE_PATH, employee_ids[employee], shift)
        except sqlite3.Error as error:
            # Undo the in-memory addition if saving fails.
            schedule.remove_shift(shift)
            print(f"Database error: {error}")
            return

    except (ValueError, TypeError) as error:
        print(f"Shift rejected: {error}")
        return

    print(f"Shift added for {employee.get_name()}")
    print(f"Duration: {shift.calculate_shift_hr()} hours")  

# Display all employee shifts in chronological order
def view_schedule():
    shifts = schedule.get_shifts()

    if not shifts:
        print("No shifts scheduled")
        return

    sorted_shifts = sorted(
        shifts,
        key=lambda shift: (
            shift.get_date(),
            datetime.strptime(
                shift.get_start_time(), "%I:%M %p"
            ).time()
        )
    )

    print("\n--- Employee Schedule ---")

    for shift in sorted_shifts:
        employee = shift.get_employee()

        print(
            f"{shift.get_date()} | "
            f"{employee.get_name()} | "
            f"{shift.get_start_time()} - {shift.get_end_time()} | "
            f"{shift.calculate_shift_hr()} hours"
        )

# Load saved shifts using the same Employee objects held by the CLI.
def load_saved_schedule():
    loaded_schedule = Schedule()

    with sqlite3.connect(DATABASE_PATH) as connection:
        rows = connection.execute(
            """
            SELECT employee_id, date, start_time, end_time
            FROM shifts
            ORDER BY id
            """
        ).fetchall()

    # Match database IDs to the existing Employee objects.
    employees_by_id = {
        employee_id: employee
        for employee, employee_id in employee_ids.items()
    }

    for employee_id, date, start_time, end_time in rows:
        employee = employees_by_id[employee_id]
        shift = Shift(employee, date, start_time, end_time)

        # Restore saved shifts without rechecking employee availability.
        loaded_schedule.restore_shift(shift)

    return loaded_schedule



# Main menu loop
def main():
    global employees, schedule

    initialize_database(DATABASE_PATH)

    saved_employees = load_all_employees(DATABASE_PATH)

    employees = []
    employee_ids.clear()

    for employee_id, employee in saved_employees:
        employees.append(employee)
        employee_ids[employee] = employee_id

    # Restore saved shifts after loading employees and their availability.
    schedule = load_saved_schedule()

    while True:

            print("\n--- ShiftFlow V1 ---")
            print("1. Add Employee")
            print("2. Search Employee")
            print("3. View Employees")
            print("4  view employee")
            print("5. Update Employee Availability")
            print("6. Delete Employee")
            print("7. Update Employee Role")
            print("8. Remove Employee Availability")
            print("9. print Number of employees")
            print("10. Clear Availability")
            print("11. View amount of crew/sl/kl")
            print("12. Create Shift")
            print("13. View Schedule")
            print("14. Exit")

    
            try:
                choice = int(input("Enter your choice: "))  # Convert input to number
            except ValueError:
                print("Please enter a number.")  # Runs if user enters text
                continue  # Restart menu loop

            if choice == 1:
                add_employee()  # Run add employee

            elif choice == 2:
                search_employee()  # Run employee search

            elif choice == 3:
                view_employees()  # Show all employees
            
            elif choice == 4:
                view_employee()
                
            elif choice == 5:
                update_availability()  # Update availability
            
            elif choice == 6:
                delete_employee() #delete employee
            
            elif choice == 7:
                update_role() #Upadate role
            
            elif choice == 8:
                remove_availability() #remove availability
            elif choice == 9:
                employee_count() # count employee
            elif choice == 10:
                clear_availability() #clear availability
            elif choice == 11:
                number_role_types()
            elif choice == 12:
                create_shift()  # Create and save a new employee shift

            elif choice == 13:
                view_schedule()  # Display all scheduled shifts

            elif choice == 14:
                print("Goodbye")
                break
if __name__ == "__main__":
     main()