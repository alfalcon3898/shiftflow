from employee import Employee
class Shift:
    def __init__(self, employee:Employee, date:str, start_time:str, end_time:str ) -> None:
        self.__employee = employee
        self.__date = date
        self.__start_time = start_time
        self.__end_time = end_time
