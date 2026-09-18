from shift import Shift
class Schedule:
    """Manages a collection of employee shifts."""
    def __init__(self) -> None:
        self.__shifts = []
    def add_shift(self, shift:Shift)->None:
        if not isinstance(shift,Shift):
            raise TypeError("Shift must be a Shift object.")
        self.__shifts.append(shift)

    def get_shifts(self)->list:
        return self.__shifts.copy()
    def remove_shift(self,shift:Shift)->None:
         if not isinstance(shift,Shift):
            raise TypeError("Shift must be a Shift object.")
         
         self.__shifts.remove(shift)




