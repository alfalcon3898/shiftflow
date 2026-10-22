from fastapi import FastAPI, HTTPException
from database import load_employee


def create_app(database_path):
    # Build the API app; database_path will be used for employee lookups.
    app = FastAPI()

    # Route GET requests such as /employees/3 to the function below.
    @app.get("/employees/{employee_id}")
    def get_employee(employee_id: int):

        #Load the employee object from database supplied to create_app

        employee = load_employee(database_path, employee_id)

        if employee is None:
            raise HTTPException(status_code=404, detail= "Employee not found")

        #read the employee's data through its public getters.
        return{
            "id": employee_id,
            "name": employee.get_name(),
            "role": employee.get_role(),
            "target_weekly_hr": employee.get_target_weekly_hr(),
            "hire_date": employee.get_hire_date(),
            "availability": employee.get_availability()
        }

    # Give the configured app back to the caller, such as our test.
    return app