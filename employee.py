class Employee:
    """Represents a single employee with encapsulated name, role, and availability data."""
    def __init__(self,name:str, role:str) -> None:
        self.__name = name   # private — must go through get_name()
        self.__role = role   # private — must go through get_role()

        self.__availability = [] # private — starts empty, grows via add_availability()
    
    # --- Getters ---

    def get_name(self) -> str:
        return self.__name
    def get_role(self) -> str:
        return self.__role
    def get_availability(self) ->list[str]:  
        return self.__availability
    
    # --- Setters ---
    def set_role(self, role:str) -> None:
        self.__role = role

    def add_availability(self, availability_slot: str) -> None:
        self.__availability.append(availability_slot)




