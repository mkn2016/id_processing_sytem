import sys

from africastalking.Service import AfricasTalkingException


class StudentKeyError(BaseException):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "testing this shit"


class AfricasTalkingError(AfricasTalkingException):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Encountered an error while trying to send message"


class NullValueError(BaseException):
    def __init__(self, key):
        self.key = key
        super().__init__(self.key)

    def __str__(self):
        return "{} can not be empty".format(self.key)


def without_traceback_handler(exception_type, exception_value, exception_traceback):
    exception_traceback_handler = [StudentKeyError, NullValueError, AfricasTalkingError]

    if exception_type in exception_traceback_handler:
        print('{0}: {1}'.format(exception_type.__name__, exception_value))
    else:
        sys.__excepthook__(exception_type, exception_value, exception_traceback)


sys.excepthook = without_traceback_handler
