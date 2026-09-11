class Employee:
    """Represents a single employee with encapsulated name, role, and availability data."""
    def __init__(self,name:str, role:str) -> None:
        if name.strip() == "":
            raise ValueError("Employee name cannot be empty.")
        if len(name) > 100:
            raise ValueError("Employee name is unreasonably long.")
        self.__name = name   # private — must go through get_name()

        if role.strip() == "":
            raise ValueError("Role cannot be empty")
        
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
    
    # --- Adder ---

    def add_availability(self, availability_slot: str) -> None: #add this time slot to the employee's availability list
        self.__availability.append(availability_slot)
    
    #--- Remover --

    def remove_availability(self, availability_slot: str) -> None:
         # check membership before removing — avoids a crash if the slot isn't present,
         # and gives a clear, specific error instead of a generic Python exception
         if availability_slot in self.__availability:
                self.__availability.remove(availability_slot)
         else: 
            raise ValueError(f"{self.__name} does not have '{availability_slot}' in their availability.")
         
    # --- Clearer --
    def clear_availability(self) ->None:
        self.__availability.clear()






