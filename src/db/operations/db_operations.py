from functools import wraps
from typing import Union, Callable

from rethinkdb import r, errors

from src.db.connection.connection import RethinkDBConnection


class RethinkDBOperations(object):
    def __init__(self, **kwargs):
        self.__kwargs = kwargs
        self.__operator = None
        self.__response = {"result": None, "msg": None}

    @property
    def all_databases(self) -> list:
        with RethinkDBConnection(**self.__kwargs) as con:
            try:
                databases = r.db_list().run(con)
            except errors.ReqlDriverError:
                databases = []
            except:
                databases = []

        return databases

    def database_doesnt_exist(func):
        @wraps(func)
        def wrapper(self, *args):
            if args[0] in self.all_databases:
                self.__response["msg"] = "Database already exists"
                return self.__response
            else:
                return func(self, *args)
        return wrapper

    def database_exists(func):
        @wraps(func)
        def wrapper(self, *args):
            if not args[0] in self.all_databases:
                self.__response["msg"] = "Database doesnt exist"
                return self.__response
            else:
                return func(self, *args)
        return wrapper

    @database_doesnt_exist
    def create_database(self, database) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            try:
                r.db_create(database).run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Database not created. Driver error."
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Database creation failed. Something must have happened while trying to create the table"
            except AttributeError:
                self.__response[
                    "msg"] = "Database creation failed. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Database created successfully"

        return self.__response

    @database_exists
    def all_tables(self, database) -> list:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                tables = r.table_list().run(con)
            except errors.ReqlDriverError:
                tables = []
            except:
                tables = []

        return tables

    def table_exists(func) -> Union[dict, Callable]:
        @wraps(func)
        def wrapper(self, *args):
            if not args[1] in self.all_tables(args[0]):
                self.__response["msg"] = "table does not exist"
                return self.__response
            else:
                return func(self, *args)
        return wrapper

    def table_does_not_exist(func) -> Union[dict, Callable]:
        @wraps(func)
        def wrapper(self, *args):
            if args[1] in self.all_tables(args[0]):
                self.__response["msg"] = "table already exists"
                return self.__response
            else:
                return func(self, *args)

        return wrapper

    def table_is_not_empty(func) -> Union[dict, Callable]:
        @wraps(func)
        def wrapper(self, *args):
            if not self.table_docs(args[0], args[1]):
                self.__response["msg"] = "table is empty"
                return self.__response
            else:
                return func(self, *args)
        return wrapper

    def id_does_not_exist(func) -> Union[dict, Callable]:
        @wraps(func)
        def wrapper(self, *args):
            if args[2]["id"] in [doc["id"] for doc in self.table_docs(args[0], args[1])]:
                self.__response["msg"] = "Document with that id already exists"
                return self.__response
            else:
                return func(self, *args)
        return wrapper

    def id_exists(func) -> Union[dict, Callable]:
        @wraps(func)
        def wrapper(self, *args):
            if not args[2] in [doc["id"] for doc in self.table_docs(args[0], args[1])]:
                self.__response["msg"] = "Document with that id does not exist"
                return self.__response
            else:
                return func(self, *args)
        return wrapper


    @database_exists
    @table_does_not_exist
    def create_table(self, database, table) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                r.table_create(table).run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Table not created. Driver error."
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Table creation failed. Something must have happened while trying to create the table"
            except AttributeError:
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Table creation failed. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Table created successfully"

        return self.__response

    @database_exists
    @table_exists
    def delete_table(self, database, table) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                r.table_drop(table).run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Table not deleted. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Table deletion failed. Something must have happened while trying to delete the table"
            except AttributeError:
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Table deletion failed. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Table deleted successfully"

        return self.__response

    @database_exists
    @table_exists
    def table_docs(self, database, table) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                table_result = [doc for doc in r.table(table).order_by("id").run(con)]
            except errors.ReqlDriverError:
                table_result = []
            except:
                table_result = []

        return table_result

    @database_exists
    @table_exists
    def order_table_docs(self, database, table, order_param) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                table_result = [doc for doc in r.table(table).order_by(order_param).run(con)]
            except errors.ReqlDriverError:
                table_result = []
            except:
                table_result = []

        return table_result

    @database_exists
    @table_exists
    @table_is_not_empty
    def order_by_and_pluck_table_docs(self, database, table, order_param, pluck_param) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                pluck_param = pluck_param.split(",")
                result = r.table(table).order_by(order_param).pluck(pluck_param).coerce_to("array").run(con)
            except errors.ReqlDriverError:
                self.__response["msg"] = "Could not get table documents by the order and pluck params. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Could not get table documents by the order and pluck params. Something must have happened while trying to count table documents."
            except AttributeError:
                self.__response[
                    "msg"] = "Could not get table documents by the order and pluck params. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = result

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    def filter_and_order_by_and_pluck_table_docs(self, database, table, filter_param, order_param, pluck_param) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                pluck_param = pluck_param.split(",")
                result = r.table(table).filter(filter_param).order_by(order_param).pluck(pluck_param).coerce_to("array").run(con)
            except errors.ReqlDriverError:
                self.__response["msg"] = "Could not get table documents by the filter, order and pluck param. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Could not get table documents by the filter, order and pluck param. Something must have happened while trying to count table documents."
            except AttributeError:
                self.__response[
                    "msg"] = "Could not get table documents by the filter, order and pluck param. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = result

        return self.__response


    @database_exists
    @table_exists
    @id_does_not_exist
    def insert_doc_to_table(self, database, table, doc) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                r.table(table).insert(doc).run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Document not inserted. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Document not inserted. Something must have happened while trying to indert document to table"
            except AttributeError:
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Document not inserted. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Document inserted successfully"

        return self.__response

    @database_exists
    @table_exists
    def update_doc(self, database, table, doc, doc_id) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                r.table(table).get(doc_id).update(doc).run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Document not updated. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Document not updated. Something must have happened while trying to update document to table"
            except AttributeError:
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Document not updated. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Document updated successfully"

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    @id_exists
    def get_doc_by_id(self, database, table, doc_id) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                doc_result = r.table(table).get(doc_id).run(con)
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["msg"] = "Document not found. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Document not found. Something must have happened while trying to retrieve document"
            except AttributeError:
                self.__response[
                    "msg"] = "Document not found. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"

            if doc_result is None:
                self.__response["msg"] = "Document matching that id was not found"
            else:
                self.__response["result"] = doc_result
                self.__response["msg"] = "Document found"

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    def delete_all_docs(self, database, table) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                r.table(table).delete().run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Deletion failed. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Deletion falied. Something must have happened while trying to delete all docs from the table"
            except AttributeError:
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Deletion failed. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Deleted all records successfully"

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    @id_exists
    def delete_doc_by_id(self, database, table, doc_id) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                r.table(table).get(doc_id).delete().run(con)
            except errors.ReqlDriverError:
                self.__response["result"] = False
                self.__response["msg"] = "Could not delete the document. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Could not delete the document. Driver error. Something must have happened while trying to delete document."
            except AttributeError:
                self.__response["result"] = False
                self.__response[
                    "msg"] = "Could not delete the document. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = True
                self.__response["msg"] = "Document deleted successfully"

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    def count_table_docs(self, database, table) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                result = r.table(table).count().run(con)
            except errors.ReqlDriverError:
                self.__response["msg"] = "Count failed. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Count failed. Driver error. Something must have happened while trying to count table documents."
            except AttributeError:
                self.__response[
                    "msg"] = "Could not delete the document. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = result

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    def filter_table_docs(self, database, table, filter_param) -> dict:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                result = [cursor for cursor in r.table(table).filter(filter_param).run(con)]
            except errors.ReqlDriverError:
                self.__response["msg"] = "Could not get table documents by the filter params. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Could not get table documents by the filter params. Something must have happened while trying to count table documents."
            except AttributeError:
                self.__response[
                    "msg"] = "Could not get table documents by the filter params. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = result

        return self.__response

    @database_exists
    @table_exists
    @table_is_not_empty
    def count_docs_by_filter(self, database, table, doc_param, operator, count_param) -> dict:
        if operator == "eq":
            func = lambda user: user[doc_param].eq(count_param)
        elif operator == "lt":
            func = lambda user: user[doc_param].lt(count_param)
        elif operator == "lte":
            func = lambda user: user[doc_param].le(count_param)
        elif operator == "gt":
            func = lambda user: user[doc_param].gt(count_param)
        elif operator == "gte":
            func = lambda user: user[doc_param].ge(count_param)

        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            try:
                count_result = r.table(table).count(func).run(con)
            except errors.ReqlDriverError:
                self.__response["msg"] = "Could not get table documents by the filter params. Driver error"
            except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                self.__response[
                    "msg"] = "Could not get table documents by the filter params. Something must have happened while trying to count table documents."
            except AttributeError:
                self.__response[
                    "msg"] = "Could not get table documents by the filter params. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
            else:
                self.__response["result"] = count_result

        return self.__response

    @database_exists
    @table_exists
    def generate_id(self, database, table) -> int:
        with RethinkDBConnection(**self.__kwargs) as con:
            con.use(database)
            if r.db(database).table(table).is_empty().run(con):
                self.__response["result"] = 1
            else:
                try:
                    id_counter = r.db(database).table(table).order_by("id").nth(-1).get_field("id").add(1).run(con)
                except errors.ReqlDriverError:
                    self.__response["msg"] = "Could not get table documents to generate id. Driver error"
                except (errors.ReqlQueryLogicError, errors.ReqlOpFailedError, errors.ReqlCompileError):
                    self.__response[
                        "msg"] = "Could not get table documents to generate id. Something must have happened while trying to count table documents."
                except AttributeError:
                    self.__response[
                        "msg"] = "Could not get table documents to generate id. Check whether query commands are correct e.g <r.tabl(table_name).run() instead of r.table(table_name).run"
                else:
                    self.__response["msg"] = "Document id generated successfully"
                    self.__response["result"] = id_counter

            return self.__response


if __name__ == "__main__":
    t = {
        "id": 3,
        "fname":"martin",
        "lname": "kibui",
        "email": "m.k.ndirangu@gmail.com",
        "password": "admin",
        "age": 35,
        "status": "deactivated"
    }

    db_con = {
        "host": "localhost",
        "port": 28015
    }
    rops = RethinkDBOperations(**db_con)
    print(rops.generate_id("id_card_processing_system", "students"))
    # print(rops.all_databases)
    # print(rops.create_database("oi"))
    # print(rops.all_tables("oi"))
    # print(rops.create_table("oil", "mine"))
    # print(rops.delete_table("oil", "mines"))
    # print(rops.table_docs("oil", "mines"))
    # print(rops.insert_doc_to_table("oil", "mines", t))
    # print(rops.get_doc_by_id("id_card_processing_system", "students", 1022033))
    # print(rops.delete_all_docs("oil", "mines"))
    # print(rops.delete_doc_by_id("oil", "mines", 3))
    # print(rops.count_table_docs("oil", "mines"))
    # print(rops.filter_table_docs("oil", "mines", {"status": "deactivated"}))
    # print(rops.count_docs_by_filter("oil", "mines", "status", "eq", "active"))