import json

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

    employee = {}  # Create an empty employee dictionary

    name = input("Enter employee name: ")  # Get employee name
    role = input("Enter employee role: ")  # Get employee role

    employee["name"] = name  # Store employee name
    employee["role"] = role  # Store employee role

    employee["availability"] = []  # Start with empty availability

    employees.append(employee)  # Add employee to list
    save_employees()
    print("Employee added")


# Search for an employee by name
def search_employee():

    found = False  # Tracks whether employee was found

    search_name = input("Enter employee name: ")  # Employee to search for

    for employee in employees:  # Loop through employee list

        if employee["name"].lower() == search_name.lower():  # Compare names

            found = True  # Employee found

            print(f"Name: {employee['name']}")  # Display name
            print(f"Role: {employee['role']}")  # Display role
            availability_text = ", ".join(employee["availability"])
            print(f"Availability: {availability_text}")

    if not found:  # Runs if employee wasn't found
        print("Employee not found")


# Display all employees and their roles
def view_employees():
     for employee in employees:  # Loop through employee list
         print(f"{employee['name']} - {employee['role']}")  # Display name and role


# Update an employee's availability
def update_availability():

    found = False  # Tracks whether employee was found
    search_name = input("Enter employee name: ")  # Employee to update

    for employee in employees:
        if employee["name"].lower() == search_name.lower():  # Compare names
            day = input("Enter employee day availability: ")  # Day to add
            time = input("Enter time: ")  # Time employee can work
            availability_entry = f"{day} {time}"  # Combines day and time
            found = True
            if availability_entry in employee["availability"]: # check for duplicates
                 print("Availability already exists")
            else:
                employee["availability"].append(availability_entry)  # Add day to availability
                save_employees()
            
                print(f"{availability_entry} added to {employee['name']}.") # Success message

    if not found:
        print("Employee not found")



#Delete employee
def delete_employee():
    found = False #Tracks weather employee was found first false
    search_name = input("Enter employee name: ") # first need to search the name you want to delete

    for employee in employees: 
        if employee["name"].lower() == search_name.lower():
            found = True
            employees.remove(employee) #remove employee 
            save_employees()
            print(f"{employee['name']} was deleted.") #sucess message
            break
        
    if not found:
        print("Employee not found ")


# Update employee update role
def update_role():
    found = False
    search_name = input("Enter employee name: ")
    for employee in employees:
        if employee["name"].lower() == search_name.lower():
            found = True
            new_role = input("Enter New employee role: ")
            employee["role"] = new_role
            save_employees()
            print(f"{employee['name']} role updated to {new_role}")
            break
    if not found:
        print("Employee not found ")

#remove availabailty 
def remove_availability():
    found = False
    search_name = input("Enter employee name: ")

    for employee in employees:
        if employee["name"].lower() == search_name.lower():
            found = True
            available_to_remove = input("What availability do you want to remove? ")

            if available_to_remove in employee["availability"]:
                employee["availability"].remove(available_to_remove)
                save_employees()
                print(f"{available_to_remove} removed from {employee['name']}")
                break
            else:
                print("They dont work that day")

    if not found:
        print("Employee not found")         



# Main menu loop
load_employees()
while True:

    print("\n--- ShiftFlow V1 ---")
    print("1. Add Employee")
    print("2. Search Employee")
    print("3. View Employees")
    print("4. Update Employee Availability")
    print("5. Delete Employee")
    print("6. Update Employee Role")
    print("7. Remove Employee Availabilty")
    print("8. Exit")

   
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
        update_availability()  # Update availability
    
    elif choice == 5:
        delete_employee() #delete employee
    
    elif choice == 6:
        update_role()
    
    elif choice == 7:
        remove_availability()

    elif choice == 8:
        print("Goodbye")
        break

    else:
        print("Invalid choice")  # Invalid menu option