import logging
from typing import NewType, Union, NoReturn

from rethinkdb import r, errors

RethinkDBCon = NewType("RethinkDBCon", r.connect())


class RethinkDBConnection(object):
    def __init__(self, **kwargs):
        self.__con = None
        self.__kwargs = kwargs

    def __enter__(self) -> Union[NoReturn, RethinkDBCon]:
        try:
            self.__con = r.connect(**self.__kwargs)
        except errors.ReqlAuthError:
            self.__con = None
        except errors.ReqlDriverError:
            self.__con = None

        if self.__con is None:
            logging.critical("Could not connect to db due to driver error. Check connection parameters <host, port, db> before attempting to connect again")
            exit(1)
        else:
            return self.__con

    def __exit__(self, exc_type, exc_val, exc_tb) -> NoReturn:
        self.__con.close()
