from employee import Employee

def test_creates_employee_with_valid_data():
    emp = Employee("Allen" , "SL")
    assert emp.get_name() == "Allen"

def test_get_role_returns_correct_role():
    emp = Employee("Allen", "SL")
    assert emp.get_role() == "SL"
    