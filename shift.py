from employee import Employee
from datetime import datetime, timedelta
class Shift:
    def __init__(self, employee:Employee, date:str, start_time:str, end_time:str ) -> None:
        if not isinstance(employee, Employee):
            raise TypeError("Employee must be an Employee object.")
        self.__employee = employee
        datetime.strptime(date, "%Y-%m-%d")
        self.__date = date
        datetime.strptime(start_time, "%I:%M %p")
        self.__start_time = start_time
        datetime.strptime(end_time, "%I:%M %p")
        self.__end_time = end_time

    #--- Getters---
    def get_employee(self)->Employee:
        return self.__employee
    def get_date(self)->str:
        return self.__date
    def get_start_time(self)->str:
        return self.__start_time
    def get_end_time(self)->str:
        return self.__end_time

    #---Setters---
    def set_date(self,date:str)-> None:
        datetime.strptime(date, "%Y-%m-%d")
        self.__date = date
    def set_start_time(self, start_time:str)-> None:
        datetime.strptime(start_time, "%I:%M %p")
        self.__start_time = start_time
    def set_end_time(self, end_time:str)-> None:
        datetime.strptime(end_time, "%I:%M %p")
        self.__end_time = end_time

    def calculate_shift_hr(self) -> float:
        start = datetime.strptime(self.__start_time, "%I:%M %p")
        end = datetime.strptime(self.__end_time,"%I:%M %p")
        if end < start:
            end = end + timedelta(days=1)
        duration = end - start
        return duration.total_seconds() / 3600

    
    


