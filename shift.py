from employee import Employee
from datetime import datetime
class Shift:
    def __init__(self, employee:Employee, date:str, start_time:str, end_time:str ) -> None:
        self.__employee = employee
        self.__date = date
        self.__start_time = start_time
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
        self.__date = date
    def set_start_time(self, start_time:str)-> None:
        self.__start_time = start_time
    def set_end_time(self, end_time:str)-> None:
        self.__end_time = end_time
    
    
    


