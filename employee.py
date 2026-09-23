from enum import Enum
from copy import deepcopy
from datetime import datetime
class AvailabilityStatus(Enum):
        AVAILABLE = "available to work" 
        UNAVAILABLE = "unavailable to work" 
        UNKNOWN = "availability not entered"
     


class Employee:
    """Represents a single employee with encapsulated name, role, and availability data."""

    def __init__(self, name: str, role: str) -> None:
        # Validate the employee's name before storing it.
        # Reject blank names and names exceeding the 100-character limit.
        if name.strip() == "":
            raise ValueError("Employee name cannot be empty.")

        if len(name) > 100:
            raise ValueError("Employee name is unreasonably long.")

        # Keep the name private so it is accessed through get_name().
        self.__name = name

        # Validate the employee's role before storing it.
        if role.strip() == "":
            raise ValueError("Role cannot be empty")

        if len(role) > 50:
            raise ValueError("Role is unreasonably long.")

        # Keep the role private so updates go through set_role(),
        # which applies the same validation rules.
        self.__role = role
        # Store each day's availability as a list of time blocks.
        self.__availability = {}

    # --- Getters ---

    def get_name(self) -> str:
        # Return the employee's name without allowing it to be changed here.
        return self.__name

    def get_role(self) -> str:
        # Return the employee's current role.
        return self.__role

    def get_availability(self) -> dict:
        """Return a copy of the employee's availability."""

        # Return a deep copy to protect the dictionary and its nested lists.
        return deepcopy(self.__availability)

    # --- Setters ---

    def set_role(self, role: str) -> None:
        # Apply the same validation used during initialization.
        # An invalid role is rejected before the existing role is replaced.
        if role.strip() == "":
            raise ValueError("Role cannot be empty")

        if len(role) > 50:
            raise ValueError("Role is unreasonably long.")

        # Update the role only after it passes validation.
        self.__role = role

    def set_all_day_availability(self, day):
        self.__availability[day] = "ALL_DAY"


    # --- Availability Management ---

    def add_availability(self, day, time_block):
        if day not in self.__availability:
            self.__availability[day] = []
        if self.__availability[day] == "ALL_DAY":
            self.__availability[day] = []
        self.__availability[day].append(time_block)


    def remove_availability(self, day, availability_slot: tuple) -> None:
        # Check whether the requested entry exists before removing it.
        if day in self.__availability and availability_slot in self.__availability[day]:
            self.__availability[day].remove(availability_slot)
            if not self.__availability[day]:
                del self.__availability[day]
        else:
            # Provide a specific error identifying the missing entry.
            raise ValueError(
                f"{self.__name} does not have '{day},{availability_slot}' in their availability."
            )

    def clear_availability(self) -> None:
        # Remove all availability entries from the dictionary.
        self.__availability.clear()

    def check_availability(self, day, time_block):
        # No Availability entered for this day
        if day not in self.__availability:
            return  AvailabilityStatus.UNKNOWN

        if self.__availability[day] == "ALL_DAY":
            return AvailabilityStatus.AVAILABLE

        #Extract the proposed shift times.
        shift_start = time_block[0]
        shift_end = time_block[1]

        #convert strings into conparable datatime objects.
        shift_start = datetime.strptime(shift_start,"%I:%M %p" )
        shift_end = datetime.strptime(shift_end,"%I:%M %p")

        #check every available time block for this day
        for available_block in self.__availability[day]:
            available_start = available_block[0]
            available_end = available_block[1]

            available_start = datetime.strptime(available_start, "%I:%M %p")
            available_end = datetime.strptime(available_end, "%I:%M %p")

            #The entired proposrd shift must fit inside one block
            if shift_start >= available_start and shift_end <= available_end:
                return AvailabilityStatus.AVAILABLE

        # No available block contained the proposed shift.
        return AvailabilityStatus.UNAVAILABLE   



        





    