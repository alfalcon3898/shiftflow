# List that stores all employees
employees = [
    {
        "name": "Allen",
        "role": "SL",
        "availability": []
    },
    {
        "name": "John",
        "role": "Crew",
        "availability": []
    }
]

# Add a new employee to the employees list
def add_employee():

    # Create an empty dictionary for one employee
    employee = {}

    # Get employee information from the user
    name = input("Enter employee name: ")
    role = input("Enter employee role: ")

    # Store the values in the dictionary
    employee["name"] = name
    employee["role"] = role

    # Every employee starts with an empty availability list
    employee["availability"] = []

    # Add the completed employee dictionary to the employees list
    employees.append(employee)


# Search for an employee by name
def search_employee():

    # Tracks whether we found the employee
    found = False

    # Ask which employee to search for
    search_name = input("Enter employee name: ")

    # Loop through every employee in the list
    for employee in employees:

        # Compare names without caring about uppercase/lowercase
        if employee["name"].lower() == search_name.lower():

            found = True

            # Display employee information
            print(f"Name: {employee['name']}")
            print(f"Role: {employee['role']}")
            print(f"Availability: {employee['availability']}")

    # If no match was found
    if not found:
        print("Employee not found")


# Display all employees and their roles
def view_employees():

    # Loop through every employee in the list
    for employee in employees:

        # Print the employee's name and role
        print(f"{employee['name']} - {employee['role']}")


# Main menu loop
while True:

    print("\n--- ShiftFlow V1 ---")
    print("1. Add Employee")
    print("2. Search Employee")
    print("3. View Employee")
    print("4. Exit")

    # Get menu selection from user
    choice = int(input("Enter your choice: "))

    # Run the selected option
    if choice == 1:
        add_employee()

    elif choice == 2:
        search_employee()

    elif choice == 3:
        view_employees()

    elif choice == 4:
        print("Goodbye")
        break

    # Handle invalid menu choices
    else:
        print("Invalid choice")