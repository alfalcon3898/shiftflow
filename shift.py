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

    def conflicts_with(self, other: "Shift") -> bool:
        #convert the current shift's date and time
        start = datetime.strptime(
            f"{self.__date} {self.__start_time}",
            "%Y-%m-%d %I:%M %p"
        )

        end = datetime.strptime(
            f"{self.__date} {self.__end_time}",
            "%Y-%m-%d %I:%M %p"
        )

        # Handle an overnight shift.
        if end < start:
            end = end + timedelta(days=1)

        # Retrieve the other shift's information.
        other_date = other.get_date()
        other_start_time = other.get_start_time()
        other_end_time = other.get_end_time()

         # Convert the other shift's date and times.
        other_start = datetime.strptime(
            f"{other_date} {other_start_time}",
            "%Y-%m-%d %I:%M %p"
        )

        other_end = datetime.strptime(
            f"{other_date} {other_end_time}",
            "%Y-%m-%d %I:%M %p"
        )

        # Handle an overnight shift for the other employee's shift.
        if other_end < other_start:
            other_end = other_end + timedelta(days=1)

        # If the shifts belong to different employees,
        # they cannot conflict with each other.
        # Stop checking and return False.
        if self.get_employee() is not other.get_employee():
         return False

        # Check whether the two shifts overlap.
        # Shift A must start before Shift B ends,
        # AND Shift B must start before Shift A ends.
        # Both conditions must be True for a conflict.
        return start < other_end and other_start < end

