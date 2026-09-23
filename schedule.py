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