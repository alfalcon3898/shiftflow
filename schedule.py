from shift import Shift
from employee import Employee,AvailabilityStatus
from datetime import datetime,timedelta
import warnings
import random

class Schedule:
    """Manages a collection of employee shifts."""

    def __init__(self) -> None:
        # Store scheduled shifts in a private list.
        # Shifts are added and removed through the methods below.
        self.__shifts = []

    #---set staffing by sales---
    def get_required_staffing(self, projected_sales:int)-> int:
        if projected_sales <= 5000:
            return 5
        else:
            return 6
        




    # --- Add Shift ---

    def add_shift(self, shift: Shift) -> None:
        # Only accept Shift objects to prevent unrelated data
        # from being added to the schedule.
        if not isinstance(shift, Shift):
            raise TypeError("Shift must be a Shift object.")

        #Get the shift's date and convert to weekday
        date = shift.get_date()
        date_obj =  datetime.strptime(date,"%Y-%m-%d")
        day = date_obj.strftime("%A")

        #Get the employee and proposed shift time
        employee = shift.get_employee()
        time_block = (shift.get_start_time(), shift.get_end_time())

        #Check wether the employee is available for this shift
        results = employee.check_availability(day,time_block)

        #reject the shift if the employee is unavialable
        if results == AvailabilityStatus.UNAVAILABLE:
            raise ValueError("Employee is unavailable for this shift.")
        if results == AvailabilityStatus.UNKNOWN:
            warnings.warn("Employee availability has not been entered.")

        # Check for conflicts with shifts already in the schedule.
 
        for existing_shift in self.__shifts:
            if shift.conflicts_with(existing_shift):
                raise ValueError("Shift cannot be added becuase it conflict with another shift")

        # Add the validated Shift object to the schedule.
        self.__shifts.append(shift)

       

    # --- Get Shifts ---

    def get_shifts(self) -> list:
        # Return a copy so callers cannot directly add or remove
        # entries from the schedule's private list.
        return self.__shifts.copy()

    # --- Remove Shift ---

    def remove_shift(self, shift: Shift) -> None:
        # Reject values that are not Shift objects.
        if not isinstance(shift, Shift):
            raise TypeError("Shift must be a Shift object.")

        # Remove the specified shift from the schedule.
        # Python raises ValueError if the shift is not present.
        self.__shifts.remove(shift)

    def get_staffing_shortage(self, required: int, current: int) ->int:
        missing = required - current
        if missing < 0:
            missing = 0

        return missing
   
    def get_employee_hours(self, employee:Employee, week_date:str | None = None)-> float:
        total_hrs = 0
        if week_date is None:
            for shift in self.__shifts:
                if shift.get_employee() == employee:
                    total_hrs += shift.calculate_shift_hr()
                
        else:

            week_date = datetime.strptime(week_date, "%Y-%m-%d")
            days = week_date.weekday()
            week_start = week_date - timedelta(days=days)
            week_end = week_start + timedelta(days=6)

            for shift in self.__shifts:
                shift_date = datetime.strptime(shift.get_date(), "%Y-%m-%d")

                if shift.get_employee() == employee and shift_date >= week_start and shift_date <= week_end:
                    total_hrs += shift.calculate_shift_hr()
        return total_hrs

    def can_assign_shift(self, employee:Employee, shift:Shift)-> bool:
        predicted_hrs_total = self.get_employee_hours(employee) + shift.calculate_shift_hr()
        if predicted_hrs_total > 40:
            return False
        else:
          return True
    def get_remaining_target_hours(self, employee: Employee) -> float:
        current_hours = self.get_employee_hours(employee)
        target_hrs = employee.get_target_weekly_hr()
        remaining_hrs = target_hrs - current_hours
        if  current_hours > target_hrs:
            return 0
        else:
            return remaining_hrs
    def choose_employee_for_hours(self,employee_1: Employee,employee_2: Employee) -> Employee:
        employee_1_remaining_hrs = self.get_remaining_target_hours(employee_1)
        employee_2_remaining_hrs = self.get_remaining_target_hours(employee_2)
        employee_1_hire_date = employee_1.get_hire_date()
        employee_2_hire_date = employee_2.get_hire_date()

        if employee_1_remaining_hrs > employee_2_remaining_hrs:
          return employee_1
        elif employee_2_remaining_hrs > employee_1_remaining_hrs:
          return employee_2
        elif employee_2_remaining_hrs == employee_1_remaining_hrs:
            if employee_1_hire_date < employee_2_hire_date:
                return employee_1
            elif employee_2_hire_date < employee_1_hire_date:
                return employee_2
            elif employee_2_hire_date == employee_1_hire_date:
                return random.choice([employee_1, employee_2])
        
    def  can_pick_up_shift(self, employee: Employee, shift: Shift) -> bool:
        predicted_hrs_total = self.get_employee_hours(employee) + shift.calculate_shift_hr()
        if predicted_hrs_total > 40:
            return False  
        else:
            shift.set_employee(employee)  
            return True
            