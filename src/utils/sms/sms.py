from typing import NoReturn, NewType
from queue import Queue
from functools import wraps

import africastalking
from requests import get, exceptions
from src.utils.errors.exceptions import AfricasTalkingError

SmsQueue = NewType("SmsQueue", Queue)


class AfricasTalkingSMS(object):
    def __init__(self):
        super().__init__()
        self.__response = {"result": None, "msg": None}
        self.__base_url = "http://www.google.com"

    def internet_availability(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                r = get(self.__base_url)
            except exceptions.ConnectionError as e:
                self.__response["result"] = "Failed"
                self.__response["msg"] = "Connection Error"
                return self.__response
            else:
                if r.status_code == 200:
                    if self.credit_balance < 0:
                        self.__reponse["msg"] = "You dont have available credit"
                        self.__response["result"] = "Failed"
                        return self.__response
                    else:
                        return func(self, *args, **kwargs)
                else:
                    self.__response["result"] = "Failed"
                    self.__response["msg"] = "Status code could not be established"
                    return self.__response
        return wrapper

    @property
    def credit_balance(self) -> float:
        app = africastalking.Application
        balance = app.fetch_application_data()
        balance = balance["UserData"]["balance"]
        return float(balance.replace("KES", "").strip())

    def available_credit(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if isinstance(self.credit_balance, float):
                if self.credit_balance < 0:
                    self.__reponse["msg"] = "You dont have available credit"
                    self.__response["result"] = "Failed"
                    return self.__response
                else:
                    return func(self, *args, **kwargs)
            elif isinstance(self.credit_balance, dict):
                return self.__response
        return wrapper

    @internet_availability
    @available_credit
    def send_message(self, message: str, phone_number: str, q: SmsQueue) -> NoReturn:
        phone_numbers = list()
        phone_numbers.append(phone_number)
        sms = africastalking.SMS
        try:
            response_result = sms.send(message, phone_numbers)
        except AfricasTalkingError as e:
            self.__response["result"] = "Failed"
            self.__response["msg"] = f"Sms could not be sent. {e}"
            q.put(self.__response)
        except ValueError as e:
            self.__response["result"] = "Failed"
            self.__response["msg"] = e
            q.put(self.__response)
        else:
            self.__response["result"] = response_result["SMSMessageData"]["Recipients"][0]["status"]
            if self.__response["result"] == "Success":
                self.__response["msg"] = "Sms sent successfully"
            else:
                self.__response["msg"] = f"Sms could not be sent. {self.__response['result']}"
            q.put(self.__response)
