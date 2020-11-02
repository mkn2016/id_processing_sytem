from datetime import datetime
from typing import NoReturn
from pathlib import Path

from rethinkdb import r
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations
from src.utils.reports.reports import GenerateReport

qdated = QDate.currentDate().toString("dd-MM-yyyy")


class ReportsForm(QDialog, RethinkDBOperations, GenerateReport):
    def __init__(self):
        QDialog.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)
        GenerateReport.__init__(self)

        self.__main_layout = None
        self.__contact_info_layout = None
        self.__button_group_layout = None
        self.__personal_info_layout = None
        self.__contact_info_group_box = None
        self.__personal_info_group_box = None
        self.__filter_grid_layout = None
        self.__all_statuses = None
        self.__active_statuses = None
        self.__deactivated_statuses = None
        self.__pending_statuses = None
        self.__date_from = None
        self.__date_to = None
        self.__calendar_date_to = None
        self.__calendar_date_from = None
        self.__default_state = {
            "all_statuses": True,
            "active_statuses": False,
            "pending_statuses": False,
            "deactivated_statuses": False,
            "from_date_from_changed": False,
            "from_date_to_changed": False
        }

        self.load_ui()

    def init_main_layout(self) -> NoReturn:
        self.__main_layout = QFormLayout()

    def init_all_statuses(self) -> NoReturn:
        self.__all_statuses = QRadioButton()

    def init_date_from(self) -> NoReturn:
        self.__date_from = QDateEdit()

    def init_date_to(self) -> NoReturn:
        self.__date_to = QDateEdit()

    def init_calendar_date_to(self) -> NoReturn:
        self.__calendar_date_to = QCalendarWidget()

    def init_calendar_date_from(self) -> NoReturn:
        self.__calendar_date_from = QCalendarWidget()

    def init_pending_statuses(self) -> NoReturn:
        self.__pending_statuses = QRadioButton()

    def init_deactivated_statuses(self) -> NoReturn:
        self.__deactivated_statuses = QRadioButton()

    def init_active_statuses(self) -> NoReturn:
        self.__active_statuses = QRadioButton()

    def init_filter_grid_layout(self) -> NoReturn:
        self.__filter_grid_layout = QGridLayout()

    def init_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout = QGridLayout()
        self.__personal_info_layout.setAlignment(Qt.AlignTop)

    def init_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout = QHBoxLayout()
        self.__contact_info_layout.setAlignment(Qt.AlignTop)

    def init_personal_info_group_box(self) -> NoReturn:
        self.__personal_info_group_box = QGroupBox()

    def init_button_group_layout(self) -> NoReturn:
        self.__button_group_layout = QHBoxLayout()

    def init_contact_info_group_box(self) -> NoReturn:
        self.__contact_info_group_box = QGroupBox()

    def setup_calendar_date_from(self) -> NoReturn:
        self.__calendar_date_from.setMaximumDate(QDate.currentDate().addDays(-365))

    def setup_calendar_date_to(self) -> NoReturn:
        self.__calendar_date_to.setMaximumDate(QDate.currentDate())
        self.__calendar_date_to.setMinimumDate(QDate.currentDate())
        self.__calendar_date_to.setDateEditEnabled(False)

    def setup_all_statuses(self) -> NoReturn:
        self.__all_statuses.setText("All")
        self.__all_statuses.toggle()
        self.__all_statuses.clicked.connect(self.on_all_statuses_clicked)

    def on_all_statuses_clicked(self) -> NoReturn:
        self.__default_state["all_statuses"] = True
        self.__default_state["active_statuses"] = False
        self.__default_state["pending_statuses"] = False
        self.__default_state["deactivated_statuses"] = False

    def setup_active_statuses(self) -> NoReturn:
        self.__active_statuses.setText("Active")
        self.__active_statuses.clicked.connect(self.on_active_statuses_clicked)

    def on_active_statuses_clicked(self) -> NoReturn:
        self.__default_state["active_statuses"] = True
        self.__default_state["all_statuses"] = False
        self.__default_state["pending_statuses"] = False
        self.__default_state["deactivated_statuses"] = False

    def setup_pending_statuses(self) -> NoReturn:
        self.__pending_statuses.setText("Pending")
        self.__pending_statuses.clicked.connect(self.on_pending_statuses_clicked)

    def on_pending_statuses_clicked(self) -> NoReturn:
        self.__default_state["pending_statuses"] = True
        self.__default_state["all_statuses"] = False
        self.__default_state["active_statuses"] = False
        self.__default_state["deactivated_statuses"] = False

    def setup_deactivated_statuses(self) -> NoReturn:
        self.__deactivated_statuses.setText("Deactivated")
        self.__deactivated_statuses.clicked.connect(self.on_deactivated_statuses_clicked)

    def on_deactivated_statuses_clicked(self) -> NoReturn:
        self.__default_state["deactivated_statuses"] = True
        self.__default_state["all_statuses"] = False
        self.__default_state["active_statuses"] = False
        self.__default_state["pending_statuses"] = False

    def setup_main_layout(self) -> NoReturn:
        self.__main_layout.setAlignment(Qt.AlignCenter)
        self.setObjectName("reportsForm")
        self.setWindowTitle("Generate Report")
        self.setFixedSize(QSize(400, 350))
        self.setLayout(self.__main_layout)

    def setup_personal_info_group_box(self) -> NoReturn:
        self.__personal_info_group_box.setTitle("Generate Report By Status")
        self.__personal_info_group_box.setFixedSize(QSize(370, 100))
        self.__personal_info_group_box.setLayout(self.__personal_info_layout)

    def setup_button_group_layout(self) -> NoReturn:
        self.__button_group_layout.addSpacing(520)
        self.__button_group_layout.setContentsMargins(0, 20, 0, 0)
        cancel_btn = QPushButton()
        cancel_btn.setText("Cancel")
        cancel_btn.setStyleSheet(
            """
            background-color: tomato;
            color: white
            """
        )
        cancel_btn.clicked.connect(self.close)

        generate_btn = QPushButton()
        generate_btn.setText("Generate")
        generate_btn.setStyleSheet(
            """
            background-color: teal;
            color: white
            """
        )
        generate_btn.clicked.connect(self.on_generate_report)

        self.__button_group_layout.addWidget(cancel_btn)
        self.__button_group_layout.addWidget(generate_btn)

    def setup_contact_info_groupbox(self) -> NoReturn:
        self.__contact_info_group_box.setContentsMargins(0, 0, 0, 0)
        self.__contact_info_group_box.setTitle("Generate Report By Date")
        self.__contact_info_group_box.setFixedSize(QSize(370, 100))
        self.__contact_info_group_box.setLayout(self.__contact_info_layout)

    def setup_date_to(self) -> NoReturn:
        self.__date_to.setDisplayFormat("dd-MM-yyyy")
        self.__date_to.setCalendarPopup(True)
        self.__date_to.setCalendarWidget(self.__calendar_date_to)
        self.__date_to.setDate(QDate.currentDate())
        self.__date_to.setMaximumDate(QDate.currentDate())
        self.__date_to.setMinimumDate(QDate.currentDate())
        self.__date_to.dateChanged.connect(self.date_to_changed)

    def setup_date_from(self) -> NoReturn:
        self.__date_from.setDisplayFormat("dd-MM-yyyy")
        self.__date_from.setCalendarPopup(True)
        self.__date_from.setCalendarWidget(self.__calendar_date_from)
        self.__date_from.setDate(QDate.currentDate())
        self.__date_from.setMaximumDate(QDate.currentDate().addDays(-365))
        self.__date_from.setMinimumDate(QDate.currentDate().addDays(-365))
        self.__date_from.dateChanged.connect(self.date_from_changed)

    def date_to_changed(self, date) -> NoReturn:
        print("date to changed")
        # print(date)
        self.__default_state["from_date_to_changed"] = True

    def date_from_changed(self, date) -> NoReturn:
        print("date from changed")
        # print(date)
        self.__default_state["from_date_from_changed"] = True

    def add_date_to_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout.addWidget(self.__date_to)

    def add_date_from_to_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout.addWidget(self.__date_from)

    def add_header_to_main_layout(self) -> NoReturn:
        header = QLabel("Generate Report")

        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(header)

        self.__main_layout.addRow("", header_layout)

    def add_personal_info_group_box_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__personal_info_group_box)

    def add_contact_info_group_box_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__contact_info_group_box)

    def add_button_group_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__button_group_layout)

    def add_all_statuses_to_person_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__all_statuses, 0, 0)

    def add_active_statuses_to_person_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__active_statuses, 0, 1)

    def add_pending_statuses_to_person_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__pending_statuses, 1, 0)

    def add_deactivated_statuses_to_person_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__deactivated_statuses, 1, 1)

    def on_generate_report(self) -> NoReturn:
        pluck_param = "id," + "first_name," + "surname," + "course," + "status," + "registered_on," + "expiry_date"

        if self.__default_state["all_statuses"]:
            if self.__default_state["from_date_from_changed"] and not self.__default_state["from_date_to_changed"]:
                print("getting all statuses and from date from changed")
            elif self.__default_state["from_date_to_changed"] and not self.__default_state["from_date_from_changed"]:
                print("getting all statuses and from date to changed")
            elif self.__default_state["from_date_from_changed"] and self.__default_state["from_date_to_changed"]:
                print("getting all statuses from date to changed and from to date changed")
            else:
                order_by_pluck_docs = self.order_by_and_pluck_table_docs(BaseConfig.db, BaseConfig.students_table, "id", pluck_param)

                if order_by_pluck_docs["result"] is None:
                    QMessageBox.critical(self, "Critical", order_by_pluck_docs["msg"])
                else:
                    if not order_by_pluck_docs["result"]:
                        pass
                    else:
                        report_result = self.generate_report(order_by_pluck_docs["result"])
                        if report_result["result"]:
                            QMessageBox.information(self, "Success", report_result["msg"])
                        else:
                            QMessageBox.critical(self, "Critical", report_result["msg"])

        elif self.__default_state["active_statuses"]:
            if self.__default_state["from_date_from_changed"] and not self.__default_state["from_date_to_changed"]:
                print("getting active statuses and from date from changed")
            elif self.__default_state["from_date_to_changed"] and not self.__default_state["from_date_from_changed"]:
                print("getting active statuses and from date to changed")
            elif self.__default_state["from_date_from_changed"] and self.__default_state["from_date_to_changed"]:
                print("getting active statuses from date to changed and from to date changed")
            else:
                filter_and_order_by_pluck_docs = self.filter_and_order_by_and_pluck_table_docs(BaseConfig.db, BaseConfig.students_table, {"status": "active"}, "id",
                                                                         pluck_param)

                if filter_and_order_by_pluck_docs["result"] is None:
                    QMessageBox.critical(self, "Critical", filter_and_order_by_pluck_docs["msg"])
                else:
                    if not filter_and_order_by_pluck_docs["result"]:
                        pass
                    else:
                        report_result = self.generate_report(filter_and_order_by_pluck_docs["result"])
                        if report_result["result"]:
                            QMessageBox.information(self, "Success", report_result["msg"])
                        else:
                            QMessageBox.critical(self, "Critical", report_result["msg"])

        elif self.__default_state["pending_statuses"]:
            if self.__default_state["from_date_from_changed"] and not self.__default_state["from_date_to_changed"]:
                print("getting pending statuses and from date from changed")
            elif self.__default_state["from_date_to_changed"] and not self.__default_state["from_date_from_changed"]:
                print("getting pending statuses and from date to changed")
            elif self.__default_state["from_date_from_changed"] and self.__default_state["from_date_to_changed"]:
                print("getting pending statuses from date to changed and from to date changed")
            else:
                filter_and_order_by_pluck_docs = self.filter_and_order_by_and_pluck_table_docs(BaseConfig.db,
                                                                                               BaseConfig.students_table,
                                                                                               {"status": "pending"},
                                                                                               "id",
                                                                                               pluck_param)

                if filter_and_order_by_pluck_docs["result"] is None:
                    QMessageBox.critical(self, "Critical", filter_and_order_by_pluck_docs["msg"])
                else:
                    if not filter_and_order_by_pluck_docs["result"]:
                        pass
                    else:
                        report_result = self.generate_report(filter_and_order_by_pluck_docs["result"])
                        if report_result["result"]:
                            QMessageBox.information(self, "Success", report_result["msg"])
                        else:
                            QMessageBox.critical(self, "Critical", report_result["msg"])

        elif self.__default_state["deactivated_statuses"]:
            if self.__default_state["from_date_from_changed"] and not self.__default_state["from_date_to_changed"]:
                print("getting deactivated statuses and from date from changed")
            elif self.__default_state["from_date_to_changed"] and not self.__default_state["from_date_from_changed"]:
                print("getting deactivated statuses and from date to changed")
            elif self.__default_state["from_date_from_changed"] and self.__default_state["from_date_to_changed"]:
                print("getting deactivated statuses from date to changed and from to date changed")
            else:
                filter_and_order_by_pluck_docs = self.filter_and_order_by_and_pluck_table_docs(BaseConfig.db,
                                                                                               BaseConfig.students_table,
                                                                                               {"status": "deactivated"},
                                                                                               "id",
                                                                                               pluck_param)

                if filter_and_order_by_pluck_docs["result"] is None:
                    QMessageBox.critical(self, "Critical", filter_and_order_by_pluck_docs["msg"])
                else:
                    if not filter_and_order_by_pluck_docs["result"]:
                        pass
                    else:
                        report_result = self.generate_report(filter_and_order_by_pluck_docs["result"])
                        if report_result["result"]:
                            QMessageBox.information(self, "Success", report_result["msg"])
                        else:
                            QMessageBox.critical(self, "Critical", report_result["msg"])

        self.reset()
        self.close()

    def reset(self) -> NoReturn:
        self.__default_state["all_statuses"] = True
        self.__default_state["active_statuses"] = False
        self.__default_state["pending_statuses"] = False
        self.__default_state["deactivated_statuses"] = False
        self.__default_state["from_date_from_changed"] = False
        self.__default_state["from_date_to_changed"] = False
        self.__all_statuses.toggle()

    def load_ui(self):
        self.init_main_layout()
        self.init_contact_info_layout()
        self.init_button_group_layout()
        self.init_personal_info_layout()
        self.init_contact_info_group_box()
        self.init_personal_info_group_box()
        self.init_all_statuses()
        self.init_active_statuses()
        self.init_pending_statuses()
        self.init_deactivated_statuses()
        self.init_date_from()
        self.init_date_to()
        self.init_calendar_date_to()
        self.init_calendar_date_from()

        self.setup_date_to()
        self.setup_date_from()
        self.setup_main_layout()
        self.setup_button_group_layout()
        self.setup_personal_info_group_box()
        self.setup_all_statuses()
        self.setup_active_statuses()
        self.setup_pending_statuses()
        self.setup_deactivated_statuses()
        self.setup_contact_info_groupbox()
        self.setup_calendar_date_from()
        self.setup_calendar_date_to()
        
        self.add_header_to_main_layout()
        self.add_personal_info_group_box_to_layout()
        self.add_all_statuses_to_person_info_layout()
        self.add_active_statuses_to_person_info_layout()
        self.add_pending_statuses_to_person_info_layout()
        self.add_deactivated_statuses_to_person_info_layout()
        self.add_contact_info_group_box_to_layout()
        self.add_date_from_to_contact_info_layout()
        self.add_date_to_contact_info_layout()
        self.add_button_group_to_layout()