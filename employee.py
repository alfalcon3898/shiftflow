from enum import Enum
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

        # Each employee starts with an empty availability list.
        # Availability is managed through the methods below.
        self.__availability = []

    # --- Getters ---

    def get_name(self) -> str:
        # Return the employee's name without allowing it to be changed here.
        return self.__name

    def get_role(self) -> str:
        # Return the employee's current role.
        return self.__role

    def get_availability(self) -> list[str]:
        """Return a copy of the employee's availability."""

        # Returning a copy prevents callers from modifying the internal list
        # without using the Employee class's availability methods.
        return self.__availability.copy()

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

    # --- Availability Management ---

    def add_availability(self, availability_slot: str) -> None:
        # Append a new availability entry to this employee's private list.
        self.__availability.append(availability_slot)

    def remove_availability(self, availability_slot: str) -> None:
        # Check whether the requested entry exists before removing it.
        if availability_slot in self.__availability:
            self.__availability.remove(availability_slot)
        else:
            # Provide a specific error identifying the missing entry.
            raise ValueError(
                f"{self.__name} does not have '{availability_slot}' in their availability."
            )

    def clear_availability(self) -> None:
        # Remove all availability entries while keeping the same list object.
        self.__availability.clear()