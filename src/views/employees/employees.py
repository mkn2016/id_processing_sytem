from datetime import datetime
from itertools import repeat
from typing import NoReturn

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations


class EmployeesPage(QWidget, RethinkDBOperations):
    def __init__(self):
        QWidget.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)

        self.__form_widget, \
        self.__form_layout, \
        self.__table, \
        self.__frame, \
        self.__header, \
        self.__container, \
        self.__main_layout, \
        self.__holder_layout, \
        self.__first_name, \
        self.__last_name, \
        self.__password1, \
        self.__password2, \
        self.__button_widget, \
        self.__button_layout, \
        self.__status, \
        self.__role, \
        self.__item_id, \
        self.__cancel_btn, \
        self.__submit_btn = repeat(None, 19)
        self.__edit_event = False
        self.__add_event = True

        self.load_ui()

    def init_status(self) -> NoReturn:
        self.__status = QComboBox()

    def init_cancel_btn(self) -> NoReturn:
        self.__cancel_btn = QPushButton()

    def init_button_layout(self) -> NoReturn:
        self.__button_layout = QHBoxLayout()

    def init_button_widget(self) -> NoReturn:
        self.__button_widget = QWidget()

    def init_submit_btn(self) -> NoReturn:
        self.__submit_btn = QPushButton()

    def init_form_layout(self) -> NoReturn:
        self.__form_layout = QVBoxLayout()

    def init_first_name(self) -> NoReturn:
        self.__first_name = QLineEdit()

    def init_last_name(self) -> NoReturn:
        self.__last_name = QLineEdit()

    def init_password1(self) -> NoReturn:
        self.__password1 = QLineEdit()

    def init_password2(self) -> NoReturn:
        self.__password2 = QLineEdit()

    def init_role(self) -> NoReturn:
        self.__role = QComboBox()

    def init_form_widget(self) -> NoReturn:
        self.__form_widget = QWidget()

    def init_table(self) -> NoReturn:
        self.__table = QTableWidget()

    def init_frame(self) -> NoReturn:
        self.__frame = QFrame(self)

    def init_header(self) -> NoReturn:
        self.__header = QHBoxLayout()

    def init_container(self) -> NoReturn:
        self.__container = QFormLayout()

    def init_main_layout(self) -> NoReturn:
        self.__main_layout = QVBoxLayout()

    def init_holder_layout(self) -> NoReturn:
        self.__holder_layout = QHBoxLayout()

    def showEvent(self, e) -> NoReturn:
        self.load_admins_table_data()

    def enterEvent(self, e) -> NoReturn:
        self.load_admins_table_data()

    def setup_main_layout(self):
        self.setStyleSheet(
            """
                QTableWidget {
                    background-color: white;
                    border: 1px solid black;
                }
                QHeaderView::section {
                    background-color: white;
                    color: black;
                }
                QLineEdit{
                    border:1px solid black;
                }
            """
        )
        self.setLayout(self.__main_layout)

    def setup_frame(self) -> NoReturn:
        self.__frame.setFrameShape(QFrame.StyledPanel)
        self.__frame.setLineWidth(1)
        self.__frame.setStyleSheet(
            """
            color: gainsboro;
            """
        )

    def setup_container(self) -> NoReturn:
        self.__frame.setLayout(self.__container)

    def setup_header(self) -> NoReturn:
        header_title = QLabel()
        header_title.setText("Employees")
        header_title.setStyleSheet(
            """
            color: black;
            font-size: 20px;
            """
        )

        page_title = QLabel()
        page_title.setText("Dashboard/Employees")
        page_title.setStyleSheet(
            """
            color: black;
            font-size: 12px;
            """
        )

        self.__header.addWidget(header_title)
        self.__header.addStretch(1)
        self.__header.addWidget(page_title)

    def setup_holder_layout(self) -> NoReturn:
        self.__holder_layout.setContentsMargins(0, 0, 0, 0)

    def setup_form_widget(self) -> NoReturn:
        self.__form_widget.setFixedWidth(200)
        self.__form_widget.setStyleSheet(
            """
            """
        )
        self.__form_widget.setLayout(self.__form_layout)

    def setup_table(self) -> NoReturn:
        self.__table.setRowCount(0)
        self.__table.setColumnCount(8)
        self.__table.setStyleSheet(
            """
            QTableWidget{
                color: black;
            }
            """
        )
        self.__table.setAlternatingRowColors(True)

        self.__table.setColumnWidth(0, 50)
        self.__table.setColumnWidth(1, 150)
        self.__table.setColumnWidth(2, 150)
        self.__table.setColumnWidth(3, 150)
        self.__table.setColumnWidth(4, 150)
        self.__table.setColumnWidth(5, 150)
        self.__table.setColumnWidth(6, 150)
        self.__table.setColumnWidth(7, 150)

        self.__table.horizontalHeader().setCascadingSectionResizes(False)
        self.__table.horizontalHeader().setSortIndicatorShown(False)
        self.__table.horizontalHeader().setStretchLastSection(True)

        self.__table.verticalHeader().setVisible(False)
        self.__table.verticalHeader().setCascadingSectionResizes(False)
        self.__table.verticalHeader().setStretchLastSection(False)
        self.__table.setFocusPolicy(Qt.NoFocus)
        self.__table.setSelectionMode(QAbstractItemView.NoSelection)
        self.__table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.__table.setHorizontalHeaderLabels(
            ("", "", "", "", "", "", "", ""))

        id_ = self.__table.horizontalHeaderItem(0)
        id_.setIcon(QIcon("../icons/id1.png"))
        id_.setText("Id No")

        first_name = self.__table.horizontalHeaderItem(1)
        first_name.setIcon(QIcon("../icons/employee_first_name.png"))
        first_name.setText("First name")

        last_name = self.__table.horizontalHeaderItem(2)
        last_name.setIcon(QIcon("../icons/employee_last_name.png"))
        last_name.setText("Last name")

        password = self.__table.horizontalHeaderItem(3)
        password.setIcon(QIcon("../icons/employee_password.png"))
        password.setText("Password")

        status = self.__table.horizontalHeaderItem(4)
        status.setIcon(QIcon("../icons/employee_status.png"))
        status.setText("Status")

        role = self.__table.horizontalHeaderItem(5)
        role.setIcon(QIcon("../icons/employee_role.png"))
        role.setText("Role")

        date_created = self.__table.horizontalHeaderItem(6)
        date_created.setIcon(QIcon("../icons/employee_date_created.png"))
        date_created.setText("Date Created")

        date_modified = self.__table.horizontalHeaderItem(7)
        date_modified.setIcon(QIcon("../icons/employee_date_modified.png"))
        date_modified.setText("Date Modified")

    def setup_form_layout(self) -> NoReturn:
        self.__form_layout.setContentsMargins(0, 0, 0, 0)
        self.__form_layout.setAlignment(Qt.AlignTop)

    def setup_first_name(self) -> NoReturn:
        self.__first_name.setContentsMargins(0, 0, 0, 0)
        self.__first_name.setPlaceholderText("Enter Firstname")
        self.__first_name.setStyleSheet(
            """
            color: black
            """
        )

    def setup_last_name(self) -> NoReturn:
        self.__last_name.setContentsMargins(0, 0, 0, 0)
        self.__last_name.setPlaceholderText("Enter Lastname")
        self.__last_name.setStyleSheet(
            """
            color: black
            """
        )

    def setup_password1(self) -> NoReturn:
        self.__password1.setContentsMargins(0, 0, 0, 0)
        self.__password1.setPlaceholderText("Enter Password")
        self.__password1.setStyleSheet(
            """
            color: black
            """
        )
        self.__password1.setEchoMode(QLineEdit.Password)

    def setup_password2(self) -> NoReturn:
        self.__password2.setContentsMargins(0, 0, 0, 0)
        self.__password2.setPlaceholderText("Confirm Password")
        self.__password2.setStyleSheet(
            """
            color: black
            """
        )
        self.__password2.setEchoMode(QLineEdit.Password)

    def setup_status(self) -> NoReturn:
        self.__status.setFixedHeight(25)
        self.__status.setContentsMargins(0, 0, 0, 0)
        self.__status.addItems([
            "deactivated",
            "suspended",
            "active"
        ])
        self.__status.setCurrentText("active")
        self.__status.setStyleSheet(
            """
            border-radius: 1;
            color: black;
            border: 1px solid black;
            """
        )

    def setup_role(self) -> NoReturn:
        self.__role.setFixedHeight(25)
        self.__role.setContentsMargins(0, 0, 0, 0)
        self.__role.addItems([
            "admin",
            "moderator",
        ])
        self.__role.setCurrentText("admin")
        self.__role.setStyleSheet(
            """
            border-radius: 1;
            color: black;
            border: 1px solid black;
            """
        )

    def setup_submit_btn(self) -> NoReturn:
        self.__submit_btn.setText("Save")
        self.__submit_btn.setStyleSheet(
            """
            color: black;
            border" 1px solid black;
            """
        )
        self.__submit_btn.clicked.connect(self.on_submit)

    def setup_cancel_btn(self) -> NoReturn:
        self.__cancel_btn.setText("Cancel")
        self.__cancel_btn.setStyleSheet(
            """
            color: black;
            border" 1px solid black;
            """
        )
        self.__cancel_btn.clicked.connect(self.reset)

    def setup_button_widget(self) -> NoReturn:
        self.__button_widget.setContentsMargins(0, 0, 0, 0)
        self.__button_widget.setLayout(self.__button_layout)

    def setup_button_layout(self) -> NoReturn:
        self.__button_layout.setContentsMargins(0, 0, 0, 0)

    def on_submit(self) -> NoReturn:
        if self.__edit_event:

            first_name = self.__first_name.text()
            last_name = self.__last_name.text()
            status = self.__status.currentText()
            role = self.__role.currentText()

            if not (first_name or last_name):
                QMessageBox.critical(self, "Critical", "Missing one or more required parameters.")
            else:
                doc = self.get_doc_by_id(BaseConfig.db, BaseConfig.admin_table, int(self.__item_id))

                employee_id = doc["result"]["id"]

                employee_doc = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "status": status,
                    "role": role,
                    "date_modified": datetime.today().strftime("%d-%m-%Y %H:%M:%S")
                }

                doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.admin_table, employee_doc,
                                                    employee_id)
                if doc_update_result["result"]:
                    QMessageBox.information(self, "Success", "Employee updated successfully")
                    self.reset()
                else:
                    QMessageBox.critical(self, "Critical", doc_update_result["msg"])
                    self.reset()
        elif self.__add_event:
            first_name = self.__first_name.text()
            last_name = self.__last_name.text()
            password = self.__password1.text()
            confirm_password = self.__password2.text()
            status = self.__status.currentText()
            role = self.__role.currentText()

            if not (first_name and last_name and password and confirm_password):
                QMessageBox.critical(self, "Critical", "Missing one or more required parameters.")
            else:
                if password != confirm_password or confirm_password != password:
                    QMessageBox.critical(self, "Critical", "Passwords do not match.")
                else:
                    id_result = self.generate_id(BaseConfig.db, BaseConfig.admin_table)

                    if id_result["result"] is None:
                        QMessageBox.critical(self, "Critical", id_result["msg"])
                    else:
                        employee_doc = {
                            "id": id_result["result"],
                            "first_name": first_name,
                            "last_name": last_name,
                            "password": password,
                            "status": status,
                            "role": role,
                            "date_created": datetime.today().strftime("%d-%m-%Y %H:%M:%S"),
                            "date_modified": datetime.today().strftime("%d-%m-%Y %H:%M:%S")

                        }

                        doc_insert_result = self.insert_doc_to_table(BaseConfig.db, BaseConfig.admin_table,
                                                                     employee_doc)

                        if doc_insert_result["result"]:
                            QMessageBox.information(self, "Success", "Employee saved successfully")
                            self.reset()
                        else:
                            QMessageBox.critical(self, "Critical", doc_insert_result["msg"])
                            self.reset()

    def load_admins_table_data(self) -> NoReturn:
        admins_docs = self.table_docs(BaseConfig.db, BaseConfig.admin_table)

        if isinstance(admins_docs, dict):
            QMessageBox.critical(self, "Critical", admins_docs["msg"])
        elif isinstance(admins_docs, list):
            if not admins_docs:
                pass
            else:
                self.__table.clearContents()
                self.__table.setRowCount(0)

                for row_no, row_data in enumerate(admins_docs):
                    self.__table.insertRow(row_no)

                    id_item = QTableWidgetItem(str(row_data["id"]))
                    first_name_item = QTableWidgetItem(str(row_data["first_name"]))
                    last_name_item = QTableWidgetItem(str(row_data["last_name"]))
                    password_item = QTableWidgetItem(str(row_data["password"]))
                    status_item = QTableWidgetItem(str(row_data["status"]))
                    role_item = QTableWidgetItem(str(row_data["role"]))
                    date_created_item = QTableWidgetItem(str(row_data["date_created"]))
                    date_modified_item = QTableWidgetItem(str(row_data["date_modified"]))

                    self.__table.setItem(row_no, 0, id_item)
                    self.__table.setItem(row_no, 1, first_name_item)
                    self.__table.setItem(row_no, 2, last_name_item)
                    self.__table.setItem(row_no, 3, password_item)
                    self.__table.setItem(row_no, 4, status_item)
                    self.__table.setItem(row_no, 5, role_item)
                    self.__table.setItem(row_no, 6, date_created_item)
                    self.__table.setItem(row_no, 7, date_modified_item)

                    self.__table.setRowCount(len(admins_docs))
                self.__table.clicked.connect(self.on_cell_click)

    def on_cell_click(self) -> NoReturn:
        self.__edit_event = True
        self.__add_event = False

        index = self.__table.selectionModel().currentIndex()
        id_value = index.siblingAtColumn(0)
        first_name_value = index.siblingAtColumn(1)
        last_name_value = index.siblingAtColumn(2)
        password_value = index.siblingAtColumn(3)
        status_value = index.siblingAtColumn(4)
        role_value = index.siblingAtColumn(5)

        if self.__edit_event:
            self.__item_id = id_value.data()
            self.__first_name.setText(first_name_value.data())
            self.__last_name.setText(last_name_value.data())
            self.__password1.setText(password_value.data())
            self.__password1.setReadOnly(True)
            self.__password2.setVisible(False)
            self.__status.setCurrentText(status_value.data())
            self.__role.setCurrentText(role_value.data())

    def reset(self) -> NoReturn:
        self.__first_name.clear()
        self.__last_name.clear()
        self.__password1.clear()
        self.__password2.setVisible(True)
        self.__password2.clear()
        self.__status.setCurrentText("active")
        self.__role.setCurrentText("admin")
        self.__add_event = True
        self.__edit_event = False

    def add_header_to_container(self) -> NoReturn:
        self.__container.addRow(self.__header)

    def add_holder_layout_to_container(self) -> NoReturn:
        self.__container.addRow(self.__holder_layout)

    def add_frame_to_main_layout(self) -> NoReturn:
        self.__main_layout.addWidget(self.__frame)

    def add_table_to_holder_layout(self) -> NoReturn:
        self.__holder_layout.addWidget(self.__table)

    def add_form_widget_to_holder_layout(self) -> NoReturn:
        self.__holder_layout.addWidget(self.__form_widget)

    def add_first_name_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__first_name)

    def add_last_name_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__last_name)

    def add_password1_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__password1)

    def add_password2_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__password2)

    def add_status_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__status)

    def add_role_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__role)

    def add_button_widget_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__button_widget)

    def add_cancel_btn_to_button_layout(self) -> NoReturn:
        self.__button_layout.addWidget(self.__cancel_btn)

    def add_submit_btn_to_button_layout(self) -> NoReturn:
        self.__button_layout.addWidget(self.__submit_btn)

    def load_ui(self) -> NoReturn:
        self.init_frame()
        self.init_header()
        self.init_container()
        self.init_main_layout()
        self.init_holder_layout()
        self.init_form_widget()
        self.init_form_layout()
        self.init_table()
        self.init_first_name()
        self.init_last_name()
        self.init_status()
        self.init_role()
        self.init_submit_btn()
        self.init_cancel_btn()
        self.init_button_widget()
        self.init_button_layout()
        self.init_password1()
        self.init_password2()

        self.setup_main_layout()
        self.setup_frame()
        self.setup_container()
        self.setup_header()
        self.setup_holder_layout()
        self.setup_form_widget()
        self.setup_form_layout()
        self.setup_first_name()
        self.setup_last_name()
        self.setup_password1()
        self.setup_password2()
        self.setup_status()
        self.setup_role()
        self.setup_cancel_btn()
        self.setup_button_widget()
        self.setup_button_layout()
        self.setup_submit_btn()
        self.setup_table()

        self.add_frame_to_main_layout()
        self.add_header_to_container()
        self.add_holder_layout_to_container()
        self.add_form_widget_to_holder_layout()
        self.add_first_name_to_form_layout()
        self.add_last_name_to_form_layout()
        self.add_password1_to_form_layout()
        self.add_password2_to_form_layout()
        self.add_status_to_form_layout()
        self.add_role_to_form_layout()
        self.add_button_widget_to_form_layout()
        self.add_cancel_btn_to_button_layout()
        self.add_submit_btn_to_button_layout()
        self.add_table_to_holder_layout()
