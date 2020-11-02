from sys import argv, exit
from datetime import datetime
from collections import defaultdict

from rethinkdb import r
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from colorama import init, Fore, Style
from africastalking import initialize

from src.config.config import BaseConfig
from src.data.admin import admin_dummy_data
from src.data.branches import branches_dummy_data
from src.data.courses import courses_dummy_data
from src.data.students import students_dummy_data
from src.data.departments import departments_dummy_data
from src.controller.controller import Controller
from src.utils.encryption.encryption import PasswordHandler
from src.db.operations.db_operations import RethinkDBOperations


class MainApp(QApplication, RethinkDBOperations):
    init()

    def __init__(self, environment="development"):
        QApplication.__init__(self, argv)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)
        self.__environment = environment
        self.p = PasswordHandler()
        self.settings = QSettings(QSettings.NativeFormat, QSettings.SystemScope, 'mine', 'settings')
        self.settings.setFallbacksEnabled(False)

    def set_africastalking_init(self):
        initialize(BaseConfig.africastalking_username, BaseConfig.africastalking_apikey)

    def set_application_version(self):
        self.setApplicationVersion("1.0.0")

    def set_application_org_name(self):
        self.setOrganizationName("Martin Kibui Ndirangu")

    def set_application_name(self):
        self.setApplicationName("Student Id Card Processing System")

    def setup(self):
        self.set_application_name()
        self.set_application_version()
        self.set_application_org_name()
        self.set_africastalking_init()

    def on_load(self):
        self.controller = Controller(settings=self.settings)
        self.controller.show_login()

    def closeEvent(self, e):
        self.settings.clear()

    def run(self):
        exit(self.exec_())

    def on_startup(self):
        if self.__environment == "development":
            result, admin_dummy_data_result, students_dummy_data_result, departments_dummy_data_result, branches_dummy_data_result, courses_dummy_data_result = [defaultdict(list) for _ in range(6)]

            if not self.startingUp():
                print(Fore.GREEN + Style.BRIGHT + "[*] " + "Starting ID Processing System at: " + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "...")
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Creating database...")
                print(Fore.BLACK + "-" * 50)
                db_result = self.create_database(BaseConfig.db)
                if db_result["result"]:
                    print(Fore.GREEN + "[+] " + db_result["msg"])
                elif db_result["result"] is None:
                    print(Fore.BLUE + "[!] " + db_result["msg"])
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Creating tables...")
                print(Fore.BLACK + "-" * 50)
                for table in BaseConfig.tables:
                    result[table].append(self.create_table(BaseConfig.db, table))
                result = dict(result)
                for k, v in result.items():
                    if v[0]["result"] is None:
                        print(Fore.BLUE + "[*] " + k + " " + v[0]["msg"])
                    else:
                        print(Fore.GREEN + "[+] " + " " + k, v[0]["msg"])
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Loading admin dummy data...")
                print(Fore.BLACK + "-" * 50)
                for admin_idx, admin in enumerate(admin_dummy_data):
                    hashed_password = self.p.encrypt_password(admin["password"])
                    admin["password"] = hashed_password
                    admin_dummy_data_result[admin_idx].append(self.insert_doc_to_table(BaseConfig.db, BaseConfig.admin_table, admin))
                admin_dummy_data_result = dict(admin_dummy_data_result)
                for k, v in admin_dummy_data_result.items():
                    if v[0]["result"] is None:
                        print(Fore.BLUE + "[*] " + v[0]["msg"])
                    else:
                        print(Fore.GREEN + "[+] " + v[0]["msg"])
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Loading student dummy data...")
                print(Fore.BLACK + "-" * 50)
                for student_idx, student in enumerate(students_dummy_data):
                    print(student)
                    students_dummy_data_result[student_idx].append(
                        self.insert_doc_to_table(BaseConfig.db, BaseConfig.students_table, student))
                students_dummy_data_result = dict(students_dummy_data_result)
                for k, v in students_dummy_data_result.items():
                    if v[0]["result"] is None:
                        print(Fore.BLUE + "[*] " + v[0]["msg"])
                    else:
                        print(Fore.GREEN + "[+] " + v[0]["msg"])
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Loading departments dummy data...")
                print(Fore.BLACK + "-" * 50)
                for department_idx, department in enumerate(departments_dummy_data):
                    print(department)
                    departments_dummy_data_result[department_idx].append(
                        self.insert_doc_to_table(BaseConfig.db, BaseConfig.departments_table, department))
                departments_dummy_data_result = dict(departments_dummy_data_result)
                for k, v in departments_dummy_data_result.items():
                    if v[0]["result"] is None:
                        print(Fore.BLUE + "[*] " + v[0]["msg"])
                    else:
                        print(Fore.GREEN + "[+] " + v[0]["msg"])
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Loading branches dummy data...")
                print(Fore.BLACK + "-" * 50)
                for branch_idx, branch in enumerate(branches_dummy_data):
                    print(branch)
                    branches_dummy_data_result[branch_idx].append(
                        self.insert_doc_to_table(BaseConfig.db, BaseConfig.branches_table, branch))
                branches_dummy_data_result = dict(branches_dummy_data_result)
                for k, v in branches_dummy_data_result.items():
                    if v[0]["result"] is None:
                        print(Fore.BLUE + "[*] " + v[0]["msg"])
                    else:
                        print(Fore.GREEN + "[+] " + v[0]["msg"])
                print(Fore.BLACK + "-" * 50)

                print(Fore.BLACK + "[*] " + "Loading courses dummy data...")
                print(Fore.BLACK + "-" * 50)
                for course_idx, course in enumerate(courses_dummy_data):
                    print(course)
                    courses_dummy_data_result[course_idx].append(
                        self.insert_doc_to_table(BaseConfig.db, BaseConfig.courses_table, course))
                courses_dummy_data_result = dict(courses_dummy_data_result)
                for k, v in courses_dummy_data_result.items():
                    if v[0]["result"] is None:
                        print(Fore.BLUE + "[*] " + v[0]["msg"])
                    else:
                        print(Fore.GREEN + "[+] " + v[0]["msg"])
                print(Fore.BLACK + "-" * 50)
            else:
                print(Fore.RED + "[!] " + "Couldn't start id Processing System")
        elif self.__environment == "production":
            self.create_database(BaseConfig.db)

            for table in BaseConfig.tables:
                self.create_table(BaseConfig.db, table)

            admin_table_docs = self.table_docs(BaseConfig.db, BaseConfig.admin_table)

            if isinstance(admin_table_docs, dict):
                print(admin_table_docs["msg"])
            elif isinstance(admin_table_docs, list):
                if not admin_table_docs:
                    count, attempts, super_admin = 0, 5, {}

                    name = str(input("Enter Full Name Please: "))

                    while count < attempts:
                        password = str(input("Enter password: "))
                        confirm_password = str(input("Confirm password: "))

                        if password == confirm_password:
                            count = attempts
                            super_admin.update({"id": 1, "name": name, "password": self.p.encrypt_password(password), "status": "active", "role": "super-admin", "date_joined": r.now()})
                            self.insert_doc_to_table(BaseConfig.db, BaseConfig.admin_table, super_admin)
                        else:
                            print("[!] Passwords do not match")
                            print("[-] {attempts} attempts left".format(attempts=attempts-1))
                            count += 1
                    exit()
                else:
                    pass

    def __call__(self, *args, **kwargs):
        self.setup()

        self.on_startup()

        self.on_load()

        self.run()

    Style.RESET_ALL


if __name__ == '__main__':
    main_app = MainApp()
    main_app()
