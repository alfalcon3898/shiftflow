from shift import Shift


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