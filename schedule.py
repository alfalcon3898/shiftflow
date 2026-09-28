from shift import Shift
from employee import Employee,AvailabilityStatus
from datetime import datetime,timedelta
import warnings

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
    def get_employee_hours(self, employee:Employee)-> float:
        total_hrs = 0
        for shift in self.__shifts:
            if shift.get_employee() == employee:
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
    


    