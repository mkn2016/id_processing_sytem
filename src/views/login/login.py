from itertools import repeat
from typing import NoReturn

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.config.config import BaseConfig
from src.utils.encryption.encryption import PasswordHandler
from src.utils.audit.audit_trails import parse_audit_logs
from src.db.operations.db_operations import RethinkDBOperations


class Login(QWidget, RethinkDBOperations):
    switch_window = pyqtSignal()
    submitted = pyqtSignal(str, str)

    def __init__(self, settings):
        QWidget.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)

        self.__eid,\
        self.__password,\
        self.__login_btn,\
        self.__cancel_btn,\
        self.__login_btn_layout,\
        self.__login_form_layout,\
            = repeat(None, 6)

        self.__eid_error_label,\
        self.__password_error_label\
            = [QLabel() for _ in range(2)]
        self.settings = settings
        self.p = PasswordHandler()
        self.count = 0
        self.login_attempts = 3
        self.logins = []
        self.username = None
        self.role = None

        self.on_load()

    def init_eid(self) -> NoReturn:
        self.__eid = QLineEdit()

    def init_password(self) -> NoReturn:
        self.__password = QLineEdit()

    def init_cancel_btn(self) -> NoReturn:
        self.__cancel_btn = QPushButton()

    def init_login_btn(self) -> NoReturn:
        self.__login_btn = QPushButton()

    def init_eid_error_label(self) -> NoReturn:
        self.__eid_error_label = QLabel()

    def init_login_btn_layout(self) -> NoReturn:
        self.__login_btn_layout = QHBoxLayout()

    def init_password_error_label(self) -> NoReturn:
        self.__password_error_label = QLabel()

    def init_login_form_layout(self) -> NoReturn:
        self.__login_form_layout = QFormLayout()

    def setup_eid(self) -> NoReturn:
        int_validator = QIntValidator()
        self.__eid.setValidator(int_validator)
        self.__eid.setFixedSize(QSize(235, 30))
        self.__eid.setPlaceholderText("Employee Number...")

    def setup_password(self) -> NoReturn:
        self.__password.setFixedSize(QSize(235, 30))
        self.__password.setPlaceholderText("Password...")
        self.__password.setEchoMode(QLineEdit.Password)

    def setup_cancel_btn(self) -> NoReturn:
        self.__cancel_btn.setText("Cancel")
        self.__cancel_btn.setFixedSize(QSize(80, 40))

    def setup_login_btn(self) -> NoReturn:
        self.__login_btn.setText("Login")
        self.__login_btn.setFixedSize(QSize(80, 40))

    def setup_eid_error_label(self) -> NoReturn:
        self.__eid_error_label.setObjectName("eid_error")

    def setup_password_error_label(self) -> NoReturn:
        self.__password_error_label.setObjectName("password_error")

    def setup_login_form(self) -> NoReturn:
        self.__login_form_layout.setSpacing(5)
        self.__login_form_layout.setFormAlignment(Qt.AlignCenter)

    def setup_login_btn_layout(self) -> NoReturn:
        self.__login_btn_layout.addStretch(1)

    def add_eid_to_form_layout(self) -> NoReturn:
        self.__login_form_layout.addRow("Employee Number", self.__eid)

    def add_password_to_form_layout(self) -> NoReturn:
        self.__login_form_layout.addRow("Password", self.__password)

    def add_eid_error_label_to_form_layout(self) -> NoReturn:
        self.__login_form_layout.addRow(self.__eid_error_label)

    def add_password_error_label_to_form_layout(self) -> NoReturn:
        self.__login_form_layout.addRow(self.__password_error_label)

    def add_login_btn_layout_to_form_layout(self) -> NoReturn:
        self.__login_form_layout.addRow(self.__login_btn_layout)

    def add_login_btn_to_login_btn_layout(self) -> NoReturn:
        self.__login_btn_layout.addWidget(self.__login_btn)

    def add_cancel_btn_to_login_btn_layout(self) -> NoReturn:
        self.__login_btn_layout.addWidget(self.__cancel_btn)

    def reset(self) -> NoReturn:
        self.__eid.clear()
        self.__password.clear()
        self.__eid_error_label.clear()
        self.__password_error_label.clear()

    def showEvent(self, e) -> None:
        self.username = self.settings.value("name")
        self.role = self.settings.value("role")

    @pyqtSlot()
    def on_submit(self) -> NoReturn:
        self.__password_error_label.setVisible(False)
        self.__password_error_label.setText("Password is required.")

        self.__eid_error_label.setVisible(False)
        self.__eid_error_label.setText("Employee Number is required.")

        eid = self.__eid.text()
        password = self.__password.text()

        def on_eid_change():
            self.__eid_error_label.setVisible(False)

        def on_password_change():
            self.__password_error_label.setVisible(False)

        self.__eid.textChanged.connect(on_eid_change)
        self.__password.textChanged.connect(on_password_change)

        if not eid and not password:
            self.__eid_error_label.setVisible(True)
            self.__password_error_label.setVisible(True)
        elif eid and not password:
            self.__password_error_label.setVisible(True)
        elif not eid and password:
            self.__eid_error_label.setVisible(True)
        else:

            doc_id = int(eid)

            admin = self.get_doc_by_id(BaseConfig.db, BaseConfig.admin_table, doc_id)

            if admin["result"] is None:
                QMessageBox.critical(self, "Error", "Eid does not exist")
                self.reset()
                self.__eid.setFocus()
            else:
                if admin["result"]["status"] == "active":
                    while self.count <= self.login_attempts:
                        verification = self.p.decrypt_password(admin["result"]["password"], password)

                        if isinstance(verification, tuple):
                            if verification[1] == "Verification mismatch":
                                print(self.count)
                                result = self.login_attempts - self.count
                                QMessageBox.critical(self, "Critical", "Logged in failed. \n{0} login attempts remaining.".format(result))
                                self.reset()
                                self.__eid.setFocus()
                                self.count += 1
                                break
                            else:
                                print(self.count)
                                result = self.login_attempts - self.count
                                QMessageBox.critical(self, "Critical",
                                                     "Logged in failed. \n{0} login attempts remaining.".format(result))
                                self.reset()
                                self.__eid.setFocus()
                                self.count += 1
                                break
                        elif isinstance(verification, bool):
                            self.count, self.login_attempts = 0, 3
                            QMessageBox.information(self, "Success", "You are now Logged in")
                            self.reset()
                            self.__eid.setFocus()

                            name = admin["result"]["first_name"] + " " + admin["result"]["last_name"]
                            role = admin["result"]["role"]
                            audit_log_id = self.generate_id(BaseConfig.db, "audit_trails")

                            audit_log = parse_audit_logs(audit_log_id["result"], name, "login")

                            audit_log_result = self.insert_doc_to_table(BaseConfig.db, "audit_trails", audit_log)
                            if audit_log_result["result"] is None:
                                pass
                            else:
                                self.settings.setValue("name", name)
                                self.settings.setValue("role", role)

                                self.switch_window.emit()
                                self.submitted.emit(name, role)
                                break
                    else:
                        QMessageBox.critical(self, "Critical", "Too many login attempts. Closing down application")
                        name = admin["result"]["first_name"] + " " + admin["result"]["last_name"]

                        audit_log_id = self.generate_id(BaseConfig.db, "audit_trails")

                        audit_log = parse_audit_logs(audit_log_id["result"], name, "failed_login")

                        audit_log_result = self.insert_doc_to_table(BaseConfig.db, "audit_trails", audit_log)
                        if audit_log_result["result"] is None:
                            pass
                        self.close()
                else:
                    self.reset()
                    QMessageBox.critical(self, "Critical", "Your account has been suspended or deactivated. Contact admin for further information.\n")
                    self.__eid.setFocus()
                    self.close()

    def setup_layout(self) -> NoReturn:
        # self.setFixedSize(QSize(400, 300))
        self.setObjectName("login")
        self.setWindowTitle("Login")
        self.setStyleSheet(
            """
            #eid_error, #password_error {
                color: red;
            }
            """
        )
        self.setLayout(self.__login_form_layout)

    def load_triggers(self) -> NoReturn:
        self.__cancel_btn.clicked.connect(self.close)
        self.__login_btn.clicked.connect(self.on_submit)

    def on_load(self) -> NoReturn:
        self.init_eid()
        self.init_password()
        self.init_login_btn()
        self.init_cancel_btn()
        self.init_eid_error_label()
        self.init_login_btn_layout()
        self.init_login_form_layout()
        self.init_password_error_label()

        self.setup_eid()
        self.setup_password()
        self.setup_login_btn()
        self.setup_cancel_btn()
        self.setup_login_form()
        self.setup_eid_error_label()
        self.setup_login_btn_layout()
        self.setup_password_error_label()

        self.add_eid_to_form_layout()
        self.add_eid_error_label_to_form_layout()
        self.add_password_to_form_layout()
        self.add_password_error_label_to_form_layout()
        self.add_cancel_btn_to_login_btn_layout()
        self.add_login_btn_to_login_btn_layout()
        self.add_login_btn_layout_to_form_layout()

        self.setup_layout()
        self.load_triggers()
