from employee import Employee
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
    

