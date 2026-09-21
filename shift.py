from employee import Employee
from datetime import datetime, timedelta


class Shift:
    """Represents an employee's scheduled shift and calculates its duration."""

    def __init__(
        self,
        employee: Employee,
        date: str,
        start_time: str,
        end_time: str
    ) -> None:

        # Require an Employee object rather than an employee name or dictionary.
        # This keeps each shift associated with an actual Employee instance.
        if not isinstance(employee, Employee):
            raise TypeError("Employee must be an Employee object.")

        self.__employee = employee

        # Check that the date follows the YYYY-MM-DD format.
        # strptime() raises ValueError if the date cannot be parsed.
        datetime.strptime(date, "%Y-%m-%d")
        self.__date = date

        # Validate the start time using a 12-hour clock with AM/PM.
        # Example: "11:00 PM"
        datetime.strptime(start_time, "%I:%M %p")
        self.__start_time = start_time

        # Apply the same format validation to the end time.
        datetime.strptime(end_time, "%I:%M %p")
        self.__end_time = end_time

    # --- Getters ---

    def get_employee(self) -> Employee:
        # Return the Employee object assigned to this shift.
        return self.__employee

    def get_date(self) -> str:
        # Return the scheduled date as a string.
        return self.__date

    def get_start_time(self) -> str:
        # Return the shift's starting time.
        return self.__start_time

    def get_end_time(self) -> str:
        # Return the shift's ending time.
        return self.__end_time

    # --- Setters ---

    def set_date(self, date: str) -> None:
        # Validate the new date before replacing the existing value.
        datetime.strptime(date, "%Y-%m-%d")
        self.__date = date

    def set_start_time(self, start_time: str) -> None:
        # Reject an invalid time before updating the shift.
        datetime.strptime(start_time, "%I:%M %p")
        self.__start_time = start_time

    def set_end_time(self, end_time: str) -> None:
        # Apply the same validation to the new ending time.
        datetime.strptime(end_time, "%I:%M %p")
        self.__end_time = end_time

    # --- Shift Duration ---

    def calculate_shift_hr(self) -> float:
        # Convert the stored time strings into datetime objects
        # so Python can calculate the difference between them.
        start = datetime.strptime(self.__start_time, "%I:%M %p")
        end = datetime.strptime(self.__end_time, "%I:%M %p")

        # If the end time is earlier than the start time, treat the
        # shift as overnight and move its end time to the next day.
        # Example: 11:00 PM to 7:00 AM becomes an 8-hour shift.
        if end < start:
            end = end + timedelta(days=1)

        # Subtract the start time from the adjusted end time.
        duration = end - start

        # Convert the duration from seconds to hours.
        # Dividing by 3600 returns a float, such as 7.5 hours.
        return duration.total_seconds() / 3600