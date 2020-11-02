class Messenger(object):
    def __init__(self, student_id: str, full_name: str, status: str):
        self.__status = status
        self.__full_name = full_name
        self.__student_id = student_id

    def __str__(self) -> str:
        if self.__status == "active":
            return f"{self.__full_name} of ID Number {self.__student_id} your status is {self.__status}. Access has been granted."
        else:
            return f"{self.__full_name} of ID Number {self.__student_id} your status is now {self.__status}. Contact Admin office for support."
