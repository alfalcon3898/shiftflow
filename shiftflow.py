#list of employee
employees= []
#empty dictionary
# contains name, role and availability.

#def
#add employee
def add_employee():
    employee = {}
    name = input("Enter employee name: ")
    role = input("Enter employee role: ")

    employee["name"] = name
    employee["role"] = role
    employee["availability"] = []

    employees.append(employee)

def search_employee():
    # search
    found = False
    search_name = input("Enter employee name: ")
    for employee in employees:
        if employee["name"].lower() == search_name.lower():
            found = True
            print(f"Name: {employee['name']}")
            print(f"Role: {employee['role']}")
            print(f"Availability: {employee['availability']}")
    if not found:
        print("Employee not found")








#Menu
while True:
    print("\n--- ShiftFlow V1 ---")
    print("1. Add Employee")
    print("2. Search Employee")
    print("3. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        add_employee()
    elif choice == 2:
        search_employee()
    elif choice == 3:
        print("Goodbye")
        break
    else:
        print("Invalid choice")
