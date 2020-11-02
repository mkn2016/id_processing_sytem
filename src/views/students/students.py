from itertools import repeat
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import NoReturn

from PyQt5.QtChart import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rethinkdb import r

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations
from src.utils.messenger.message_parser import Messenger
from src.utils.qrcode.qrcode_encoder import encode_data_to_file
from src.utils.sms.sms import AfricasTalkingSMS
from src.views.reports.reports import ReportsForm
from src.views.students.add_students import AddStudentsForm
from src.views.students.edit_students import EditStudentsForm


class LoadingScreen(QDialog):
    def __init__(self):
        super().__init__()

        self.setFixedSize(QSize(200, 200))
        self.setStyleSheet(
            """
            """
        )
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)
        self.label_animation = QLabel(self)
        self.label_animation.setStyleSheet(
            """
            """
        )
        self.movie = QMovie("/home/platoschild/PythonProjects/student_management_system/icons/ajax-loader.gif")
        self.movie.setBackgroundColor(QColor("white"))
        self.label_animation.setMovie(self.movie)


class StudentsPage(QWidget, RethinkDBOperations, AfricasTalkingSMS):
    def __init__(self):
        QWidget.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)
        AfricasTalkingSMS.__init__(self)

        self.__doc, \
        self.__result, \
        self.__frame, \
        self.__header, \
        self.__container, \
        self.__searchbar, \
        self.__student_id, \
        self.__statistics, \
        self.__main_layout, \
        self.__search_input, \
        self.__students_table, \
        self.__all_students_count, \
        self.__active_students_count, \
        self.__pending_students_count, \
        self.__deactivated_students_count = repeat(None, 15)
        self.__search_event = False

        self.load_ui()

    def init_frame(self) -> NoReturn:
        self.__frame = QFrame(self)

    def init_header(self) -> NoReturn:
        self.__header = QHBoxLayout()

    def init_container(self) -> NoReturn:
        self.__container = QFormLayout()

    def init_searchbar(self) -> NoReturn:
        self.__searchbar = QFormLayout()

    def init_statistics(self) -> NoReturn:
        self.__statistics = QFormLayout()

    def init_students_table(self) -> NoReturn:
        self.__students_table = QTableWidget()
        self.__students_table.horizontalScrollBar()

    def init_main_layout(self) -> NoReturn:
        self.__main_layout = QVBoxLayout()

    def init_all_students_count(self) -> NoReturn:
        self.__all_students_count = QLabel()

    def init_active_students_count(self) -> NoReturn:
        self.__active_students_count = QLabel()

    def init_pending_students_count(self) -> NoReturn:
        self.__pending_students_count = QLabel()

    def init_deactivated_students_count(self) -> NoReturn:
        self.__deactivated_students_count = QLabel()

    def init_search_input(self) -> NoReturn:
        self.__search_input = QLineEdit()

    def showEvent(self, e):
        self.reset_statistics_and_table_data()

    def enterEvent(self, e):
        if self.__search_event:
            self.load_all_students_count()
            self.load_active_students_count()
            self.load_pending_students_count()
            self.load_deactivated_students_count()
        else:
            self.reset_statistics_and_table_data()

    def focusInEvent(self, e):
        if self.__search_event:
            self.load_all_students_count()
            self.load_active_students_count()
            self.load_pending_students_count()
            self.load_deactivated_students_count()
        else:
            self.reset_statistics_and_table_data()

    def search(self) -> NoReturn:
        self.__search_event = True

        search = self.__search_input.text()
        if not search:
            QMessageBox.information(self, "Success", "Nothing to search. Search input is empty")
        else:
            doc_result = self.get_doc_by_id(BaseConfig.db, BaseConfig.students_table, int(search))

            if doc_result["msg"] == "Document with that id does not exist":
                QMessageBox.critical(self, "Critical", "Student with that id was not found")
            else:
                QMessageBox.information(self, "Success", "Student with that id found")
                self.__doc = doc_result.copy()
                self.__search_input.clear()

                self.__students_table.setRowCount(0)
                self.__students_table.setColumnCount(9)
                self.__students_table.setAlternatingRowColors(True)
                self.__students_table.setColumnWidth(0, 100)
                self.__students_table.setColumnWidth(1, 200)
                self.__students_table.setColumnWidth(2, 100)
                self.__students_table.setColumnWidth(3, 200)
                self.__students_table.setColumnWidth(4, 200)
                self.__students_table.setColumnWidth(5, 100)
                self.__students_table.setColumnWidth(6, 100)
                self.__students_table.setColumnWidth(7, 100)
                self.__students_table.setColumnWidth(8, 250)

                self.__students_table.horizontalHeader().setCascadingSectionResizes(False)
                self.__students_table.horizontalHeader().setSortIndicatorShown(False)
                self.__students_table.horizontalHeader().setStretchLastSection(True)

                self.__students_table.verticalHeader().setVisible(False)
                self.__students_table.verticalHeader().setCascadingSectionResizes(False)
                self.__students_table.verticalHeader().setStretchLastSection(False)

                self.__students_table.setFocusPolicy(Qt.NoFocus)
                self.__students_table.setSelectionMode(QAbstractItemView.NoSelection)
                self.__students_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                self.__students_table.setHorizontalHeaderLabels(
                    ("", "", "", "", "", "", "", "", ""))

                id_ = self.__students_table.horizontalHeaderItem(0)
                id_.setIcon(QIcon("../icons/id1.png"))
                id_.setText("Id No")

                name = self.__students_table.horizontalHeaderItem(1)
                name.setIcon(QIcon("../icons/name.png"))
                name.setText("Name")

                branch = self.__students_table.horizontalHeaderItem(2)
                branch.setIcon(QIcon("../icons/location1.png"))
                branch.setText("Branch")

                course = self.__students_table.horizontalHeaderItem(3)
                course.setIcon(QIcon("../icons/course2.png"))
                course.setText("Course")

                department = self.__students_table.horizontalHeaderItem(4)
                department.setIcon(QIcon("../icons/course2.png"))
                department.setText("Department")

                status = self.__students_table.horizontalHeaderItem(5)
                status.setIcon(QIcon("../icons/status1.png"))
                status.setText("Status")

                year_joined = self.__students_table.horizontalHeaderItem(6)
                year_joined.setIcon(QIcon("../icons/year_added.png"))
                year_joined.setText("Registered On")

                expiry_date = self.__students_table.horizontalHeaderItem(7)
                expiry_date.setIcon(QIcon("../icons/year_expiring.png"))
                expiry_date.setText("Expiring On")

                actions = self.__students_table.horizontalHeaderItem(8)
                actions.setIcon(QIcon("../icons/actions1.png"))
                actions.setText("Actions")

                self.__students_table.clearContents()
                self.__students_table.setRowCount(1)

                self.__students_table.setItem(0, 0, QTableWidgetItem(str(doc_result["result"]["id"])))
                self.__students_table.setItem(0, 1, QTableWidgetItem(
                    str(doc_result["result"]["first_name"] + " " + doc_result["result"]["surname"])))
                self.__students_table.setItem(0, 2, QTableWidgetItem(str(doc_result["result"]["branch"])))
                self.__students_table.setItem(0, 3, QTableWidgetItem(str(doc_result["result"]["course"])))
                self.__students_table.setItem(0, 4, QTableWidgetItem(str(doc_result["result"]["department"])))
                self.__students_table.setItem(0, 5, QTableWidgetItem(str(doc_result["result"]["status"])))
                self.__students_table.setItem(0, 6, QTableWidgetItem(str(doc_result["result"]["registered_on"])))
                self.__students_table.setItem(0, 7, QTableWidgetItem(str(doc_result["result"]["expiry_date"])))

                button_widget = QWidget()

                button_layout = QHBoxLayout()
                button_layout.setContentsMargins(0, 0, 0, 0)

                edit_btn = QPushButton()
                edit_btn.setText("Edit")
                edit_btn.setObjectName("edit_btn")
                edit_btn.clicked.connect(self.edit_student)

                pending_btn = QPushButton()
                pending_btn.setText("Suspend")
                pending_btn.setObjectName("edit_btn")
                pending_btn.clicked.connect(self.pending_hook)

                active_btn = QPushButton()
                active_btn.setText("Activate")
                active_btn.setObjectName("active_btn")
                active_btn.clicked.connect(self.active_hook)

                deactivated_btn = QPushButton()
                deactivated_btn.setText("Deactivate")
                deactivated_btn.setObjectName("deactivated_btn")
                deactivated_btn.clicked.connect(self.deactivated_hook)

                self.__student_id = doc_result["result"]["id"]

                if doc_result["result"]["status"] == "active":
                    button_layout.addWidget(edit_btn)
                    button_layout.addWidget(pending_btn)
                    button_layout.addWidget(deactivated_btn)
                elif doc_result["result"]["status"] == "pending":
                    button_layout.addWidget(edit_btn)
                    button_layout.addWidget(active_btn)
                    button_layout.addWidget(deactivated_btn)
                elif doc_result["result"]["status"] == "deactivated":
                    button_layout.addWidget(edit_btn)
                    button_layout.addWidget(active_btn)
                    button_layout.addWidget(pending_btn)
                button_widget.setLayout(button_layout)
                self.__students_table.setCellWidget(0, 8, button_widget)

    def save_file(self, filepath):
        fh = open(filepath, 'rb')
        contents = fh.read()
        fh.close()
        doc_to_insert = {"id": self.__student_id, "filename": filepath, "file": r.binary(contents)}

        self.update_doc(BaseConfig.db, BaseConfig.files_table, doc_to_insert, self.__student_id)

    def active_hook(self) -> NoReturn:
        l = LoadingScreen()

        qrcode_data = {
            "student_id": self.__student_id,
            "status": "active",
            "expiry_date": self.__doc["result"]["expiry_date"]
        }

        to_added = "qrcode_images/" + str(self.__student_id) + ".png"
        filename = str(Path(__file__).parents[3].joinpath(to_added))
        encode_data_to_file(qrcode_data, filename)
        self.save_file(filename)

        to_update = {"status": "active"}

        doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.students_table, to_update,
                                            self.__student_id)
        if doc_update_result["result"]:
            if self.__doc["result"]["tel"] == "":
                QMessageBox.information(self, "Success", "Status updated successfully")
                self.load_student_table_data()
            else:
                first_name = self.__doc['result']['first_name'].capitalize()
                surname = self.__doc['result']['surname'].capitalize()
                full_name = f"{first_name} {surname}"
                q = Queue(maxsize=1)
                m = Messenger(self.__doc['result']['id'], full_name, "active")
                Thread(target=self.send_message, args=(str(m), self.__doc['result']['tel'], q,)).start()

                message_result = q.get()
                status_update_message = f"Student status updated successfully. {message_result['msg']}"
                QMessageBox.information(self, "Success", status_update_message)
                self.load_student_table_data()
        else:
            QMessageBox.critical(self, "Critical", doc_update_result["msg"])
            self.load_student_table_data()

    def pending_hook(self) -> NoReturn:
        qrcode_data = {
            "student_id": self.__student_id,
            "status": "pending",
            "expiry_date": self.__doc["result"]["expiry_date"]
        }
        to_added = "qrcode_images/" + str(self.__student_id) + ".png"
        filename = str(Path(__file__).parents[3].joinpath(to_added))
        encode_data_to_file(qrcode_data, filename)
        self.save_file(filename)

        to_update = {"status": "pending"}

        doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.students_table, to_update,
                                            self.__student_id)
        if doc_update_result["result"]:
            if self.__doc["result"]["tel"] == "":
                QMessageBox.information(self, "Success", "Status updated successfully")
                self.load_student_table_data()
            else:
                first_name = self.__doc['result']['first_name'].capitalize()
                surname = self.__doc['result']['surname'].capitalize()
                full_name = f"{first_name} {surname}"
                q = Queue(maxsize=1)
                m = Messenger(self.__doc['result']['id'], full_name, "pending")
                Thread(target=self.send_message, args=(str(m), self.__doc['result']['tel'], q,)).start()
                message_result = q.get()
                status_update_message = f"Student status updated successfully. {message_result['msg']}"
                QMessageBox.information(self, "Success", status_update_message)
                self.load_student_table_data()
        else:
            QMessageBox.critical(self, "Critical", doc_update_result["msg"])
            self.load_student_table_data()

    def deactivated_hook(self) -> NoReturn:
        qrcode_data = {"student_id": self.__student_id, "status": "deactivated",
                       "expiry_date": self.__doc["result"]["expiry_date"]}
        to_added = "qrcode_images/" + str(self.__student_id) + ".png"
        filename = str(Path(__file__).parents[3].joinpath(to_added))

        encode_data_to_file(qrcode_data, filename)
        self.save_file(filename)

        to_update = {"status": "deactivated"}

        doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.students_table, to_update,
                                            self.__student_id)

        if doc_update_result["result"]:
            if self.__doc["result"]["tel"] == "":
                QMessageBox.information(self, "Success", "Status updated successfully")
                self.load_student_table_data()
            else:
                first_name = self.__doc['result']['first_name'].capitalize()
                surname = self.__doc['result']['surname'].capitalize()
                full_name = f"{first_name} {surname}"
                q = Queue(maxsize=1)
                m = Messenger(self.__doc['result']['id'], full_name, "deactivated")
                Thread(target=self.send_message, args=(str(m), self.__doc['result']['tel'], q,)).start()

                message_result = q.get()
                status_update_message = f"Student status updated successfully. {message_result['msg']}"
                QMessageBox.information(self, "Success", status_update_message)
                self.load_student_table_data()
        else:
            QMessageBox.critical(self, "Critical", doc_update_result["msg"])
            self.load_student_table_data()

    def edit_student(self) -> NoReturn:
        self.load_student_table_data()
        edit_dialog = EditStudentsForm()
        edit_dialog.set_messages(self.__doc["result"]["id"], self.__doc["result"]["first_name"],
                                 self.__doc["result"]["middle_name"], self.__doc["result"]["surname"],
                                 self.__doc["result"]["gender"], self.__doc["result"]["dob"],
                                 self.__doc["result"]["id_passport"], self.__doc["result"]["address1"],
                                 self.__doc["result"]["address2"], self.__doc["result"]["city"],
                                 self.__doc["result"]["state"], self.__doc["result"]["zip"],
                                 self.__doc["result"]["country"], self.__doc["result"]["tel"],
                                 self.__doc["result"]["email"], self.__doc["result"]["course"],
                                 self.__doc["result"]["department"], self.__doc["result"]["branch"],
                                 self.__doc["result"]["status"])
        edit_dialog.exec_()

    def setup_search_input(self) -> NoReturn:
        self.__search_input.setFixedSize(368, 30)
        self.__search_input.setPlaceholderText("Enter Student Id No")
        self.__search_input.setStyleSheet(
            """
            color: black;
            font-size: 12px;
            """
        )
        self.__search_input.setAttribute(Qt.WA_MacShowFocusRect, 0)
        self.__search_input.setFocusPolicy(Qt.ClickFocus)
        self.__search_input.setFocus()
        int_validator = QIntValidator()
        self.__search_input.setValidator(int_validator)

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

    @property
    def count_active_students_count(self) -> NoReturn:
        counter = self.count_docs_by_filter(BaseConfig.db, BaseConfig.students_table, "status", "eq", "active")
        return (counter["result"], 0)[counter is None]

    @property
    def count_pending_students_count(self) -> NoReturn:
        counter = self.count_docs_by_filter(BaseConfig.db, BaseConfig.students_table, "status", "eq", "pending")
        return (counter["result"], 0)[counter is None]

    @property
    def count_deactivated_students_count(self) -> NoReturn:
        counter = self.count_docs_by_filter(BaseConfig.db, BaseConfig.students_table, "status", "eq", "deactivated")
        return (counter["result"], 0)[counter is None]

    def setup_frame(self) -> NoReturn:
        self.__frame.setFrameShape(QFrame.StyledPanel)
        self.__frame.setLineWidth(1)
        self.__frame.setStyleSheet(
            """
            
            """
        )

    def setup_statistics(self) -> NoReturn:
        statistics = QHBoxLayout()

        all_students = QFrame()
        all_students.setStyleSheet(
            """
            color: black;
            """
        )
        all_students.setFrameShape(QFrame.Box)
        all_students.setFixedSize(QSize(200, 80))

        all_students_layout = QVBoxLayout()

        all_students_label = QLabel()
        all_students_label.setText("All Ids Students")

        all_students_layout.addWidget(all_students_label)
        all_students_layout.addWidget(self.__all_students_count)
        all_students.setLayout(all_students_layout)

        activated_students = QFrame()
        activated_students.setStyleSheet(
            """
            color: teal;
            """
        )
        activated_students.setFrameShape(QFrame.Box)
        activated_students.setFixedSize(QSize(200, 80))

        activated_students_layout = QVBoxLayout()

        activated_students_label = QLabel()
        activated_students_label.setText("Activated Ids Students")
        activated_students_label.setStyleSheet(
            """
            color: black;
            """
        )

        activated_students_layout.addWidget(activated_students_label)
        activated_students_layout.addWidget(self.__active_students_count)
        activated_students.setLayout(activated_students_layout)

        pending_students = QFrame()
        pending_students.setStyleSheet(
            """
            color: orange;
            """
        )
        pending_students.setFrameShape(QFrame.Box)
        pending_students.setFixedSize(QSize(200, 80))

        pending_students_layout = QVBoxLayout()

        pending_students_label = QLabel()
        pending_students_label.setText("Pending Ids Students")
        pending_students_label.setStyleSheet(
            """
            color: black;
            """
        )

        pending_students_layout.addWidget(pending_students_label)
        pending_students_layout.addWidget(self.__pending_students_count)
        pending_students.setLayout(pending_students_layout)

        deactivated_students = QFrame()
        deactivated_students.setStyleSheet(
            """
            color: red;
            """
        )
        deactivated_students.setFrameShape(QFrame.Box)
        deactivated_students.setFixedSize(QSize(200, 80))

        deactivated_students_layout = QVBoxLayout()

        deactivated_students_label = QLabel()
        deactivated_students_label.setText("Deactivated Ids Students")
        deactivated_students_label.setStyleSheet(
            """
            color: black;
            """
        )

        deactivated_students_layout.addWidget(deactivated_students_label)
        deactivated_students_layout.addWidget(self.__deactivated_students_count)
        deactivated_students.setLayout(deactivated_students_layout)

        series = QPieSeries()
        series.append("Active", int(self.count_active_students_count))
        series.append("Pending", int(self.count_pending_students_count))
        series.append("Deactivated", int(self.count_deactivated_students_count))

        active_slice = QPieSlice()
        active_slice = series.slices()[0]
        active_slice.setExploded(True)
        active_slice.setLabelVisible(True)
        active_slice.setColor(Qt.cyan)
        active_slice.setPen(QPen(Qt.darkGreen))

        pending_slice = QPieSlice()
        pending_slice = series.slices()[1]
        pending_slice.setLabelVisible(True)
        pending_slice.setColor(Qt.yellow)
        pending_slice.setPen(QPen(Qt.darkYellow))

        deactivated_slice = QPieSlice()
        deactivated_slice = series.slices()[2]
        deactivated_slice.setLabelVisible(True)
        deactivated_slice.setPen(QPen(Qt.red))

        chart = QChart()
        chart.addSeries(series)
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setBackgroundBrush(QBrush(QColor("transparent")))
        chart.setTitle("Student Statistics Pie Chart")

        legend = chart.legend()
        legend.setAlignment(Qt.AlignRight)
        legend.setShowToolTips(True)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        chart_view.setStyleSheet(
            """
            background-color: transparent
            """
        )

        statistics.addWidget(all_students)
        statistics.addWidget(activated_students)
        statistics.addWidget(pending_students)
        statistics.addWidget(deactivated_students)
        statistics.addWidget(chart_view)

        self.__statistics.addRow(statistics)

    def setup_searchbar(self) -> NoReturn:
        searchbar_layout = QHBoxLayout()

        search_btn = QPushButton()
        search_btn.clicked.connect(self.search)
        search_btn.setText("Search")
        search_btn.setFixedHeight(30)
        search_btn.setIcon(QIcon("../icons/search2.png"))
        search_btn.setStyleSheet(
            """
            QPushButton {
                border: 2px solid #8f8f91;
                color: black;
                background-color: transparent;
            }

            QPushButton:pressed {
                background-color: transparent;
                border: 2px solid teal;
            }
            """
        )

        add_student = QPushButton()
        add_student.setObjectName("add_student")
        add_student.setStyleSheet(
            """
                QPushButton {
                    border: 2px solid #8f8f91;
                    color: black;
                    background-color: transparent;
                    border-radius: 15px;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: 2px solid teal;
                }
            """
        )
        add_student.setFixedSize(QSize(30, 30))
        add_student.setIcon(QIcon("../icons/add_stud1.png"))
        add_student.clicked.connect(self.show_add_student_dialog)

        refresh_btn = QPushButton()
        refresh_btn.setObjectName("refresh_btn")
        refresh_btn.setStyleSheet(
            """
                QPushButton {
                    border: 2px solid #8f8f91;
                    color: black;
                    background-color: transparent;
                    border-radius: 15px;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: 2px solid teal;
                }
            """
        )
        refresh_btn.setFixedSize(QSize(30, 30))
        refresh_btn.setIcon(QIcon("../icons/refresh1.png"))
        refresh_btn.clicked.connect(self.reset_statistics_and_table_data)

        generate_report_btn = QPushButton()
        generate_report_btn.setObjectName("generate_report")
        generate_report_btn.setStyleSheet(
            """
                QPushButton {
                    border: 2px solid #8f8f91;
                    color: black;
                    background-color: transparent;
                    border-radius: 15px;
                }
                QPushButton:pressed {
                    background-color: transparent;
                    border: 2px solid teal;
                }
            """
        )
        generate_report_btn.setFixedSize(QSize(30, 30))
        generate_report_btn.setIcon(QIcon("../icons/pdf2.png"))
        generate_report_btn.clicked.connect(self.show_report_dialog)

        searchbar_layout.addSpacing(150)
        searchbar_layout.addWidget(self.__search_input)
        searchbar_layout.addSpacing(5)
        searchbar_layout.addWidget(search_btn)
        searchbar_layout.addStretch(1)
        searchbar_layout.addWidget(refresh_btn)
        searchbar_layout.addWidget(generate_report_btn)
        searchbar_layout.addWidget(add_student)
        searchbar_layout.addSpacing(208)

        self.__searchbar.addRow(searchbar_layout)

    def show_report_dialog(self) -> NoReturn:
        report_dialog = ReportsForm()
        report_dialog.exec()

    def reset_statistics_and_table_data(self) -> NoReturn:
        self.load_student_table_data()
        self.load_all_students_count()
        self.load_active_students_count()
        self.load_pending_students_count()
        self.load_deactivated_students_count()

    def setup_container(self) -> NoReturn:
        self.__frame.setLayout(self.__container)

    def setup_students_table(self) -> NoReturn:
        self.__students_table.setStyleSheet(
            """
            QTableWidget{
                color: black;
            }
            #edit_btn {
                color: black;
                border: 1px solid black;
                margin, padding: 0;
            }
            #active_btn {
                color: black;
                border: 1px solid black;
                margin, padding: 0;
            }
            #pending_btn {
                color: black;
                border: 1px solid black;
                margin, padding: 0;
            }
            #deactivated_btn {
                color: black;
                border: 1px solid black;
                margin, padding: 0;
            }
            """
        )

    def load_all_students_count(self) -> NoReturn:
        all_students_result = self.count_table_docs(BaseConfig.db, BaseConfig.students_table)

        if all_students_result["result"] is None:
            self.__all_students_count.setText("---")
        else:
            self.__all_students_count.setText(str(all_students_result["result"]))

    def load_active_students_count(self) -> NoReturn:
        activated_students_result = self.count_docs_by_filter(BaseConfig.db, BaseConfig.students_table, "status", "eq",
                                                              "active")

        if activated_students_result["result"] is None:
            self.__active_students_count.setText("---")
        else:
            self.__active_students_count.setText(str(activated_students_result["result"]))

    def load_pending_students_count(self) -> NoReturn:
        pending_students_result = self.count_docs_by_filter(BaseConfig.db, BaseConfig.students_table, "status", "eq",
                                                            "pending")

        if pending_students_result["result"] is None:
            self.__pending_students_count.setText("---")
        else:
            self.__pending_students_count.setText(str(pending_students_result["result"]))

    def load_deactivated_students_count(self) -> NoReturn:
        deactivated_students_result = self.count_docs_by_filter(BaseConfig.db, BaseConfig.students_table, "status",
                                                                "eq", "deactivated")
        if deactivated_students_result["result"] is None:
            self.__deactivated_students_count.setText("---")
        else:
            self.__deactivated_students_count.setText(str(deactivated_students_result["result"]))

    def load_student_table_data(self) -> NoReturn:
        students_docs = self.table_docs(BaseConfig.db, BaseConfig.students_table)

        if isinstance(students_docs, dict):
            QMessageBox.critical(self, "Critical", students_docs["msg"])
        elif isinstance(students_docs, list):
            if not students_docs:
                pass
            else:
                self.__students_table.clearContents()

                self.__students_table.setRowCount(0)
                self.__students_table.setColumnCount(8)
                self.__students_table.setAlternatingRowColors(True)

                self.__students_table.setColumnWidth(0, 100)
                self.__students_table.setColumnWidth(1, 230)
                self.__students_table.setColumnWidth(2, 100)
                self.__students_table.setColumnWidth(3, 250)
                self.__students_table.setColumnWidth(4, 200)
                self.__students_table.setColumnWidth(5, 100)
                self.__students_table.setColumnWidth(6, 100)
                self.__students_table.setColumnWidth(7, 200)
                self.__students_table.setColumnWidth(8, 100)

                self.__students_table.horizontalHeader().setCascadingSectionResizes(False)
                self.__students_table.horizontalHeader().setSortIndicatorShown(False)
                self.__students_table.horizontalHeader().setStretchLastSection(True)

                self.__students_table.verticalHeader().setVisible(False)
                self.__students_table.verticalHeader().setCascadingSectionResizes(False)
                self.__students_table.verticalHeader().setStretchLastSection(False)

                self.__students_table.setFocusPolicy(Qt.NoFocus)
                self.__students_table.setSelectionMode(QAbstractItemView.NoSelection)
                self.__students_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

                self.__students_table.setHorizontalHeaderLabels(
                    ("", "", "", "", "", "", "", ""))

                id_ = self.__students_table.horizontalHeaderItem(0)
                id_.setIcon(QIcon("../icons/id1.png"))
                id_.setText("Id No")

                name = self.__students_table.horizontalHeaderItem(1)
                name.setIcon(QIcon("../icons/name.png"))
                name.setText("Name")

                branch = self.__students_table.horizontalHeaderItem(2)
                branch.setIcon(QIcon("../icons/location1.png"))
                branch.setText("Branch")

                course = self.__students_table.horizontalHeaderItem(3)
                course.setIcon(QIcon("../icons/course2.png"))
                course.setText("Course")

                department = self.__students_table.horizontalHeaderItem(4)
                department.setIcon(QIcon("../icons/course2.png"))
                department.setText("Department")

                status = self.__students_table.horizontalHeaderItem(5)
                status.setIcon(QIcon("../icons/status1.png"))
                status.setText("Status")

                year_joined = self.__students_table.horizontalHeaderItem(6)
                year_joined.setIcon(QIcon("../icons/year_added.png"))
                year_joined.setText("Registered On")

                expiry_date = self.__students_table.horizontalHeaderItem(7)
                expiry_date.setIcon(QIcon("../icons/year_expiring.png"))
                expiry_date.setText("Expiring On")

                for row_no, row_data in enumerate(students_docs):
                    self.__students_table.insertRow(row_no)

                    self.__students_table.setItem(row_no, 0, QTableWidgetItem(str(row_data["id"])))
                    self.__students_table.setItem(row_no, 1, QTableWidgetItem(
                        str(row_data["first_name"] + " " + row_data["surname"])))
                    self.__students_table.setItem(row_no, 2, QTableWidgetItem(str(row_data["branch"])))
                    self.__students_table.setItem(row_no, 3, QTableWidgetItem(str(row_data["course"])))
                    self.__students_table.setItem(row_no, 4, QTableWidgetItem(str(row_data["department"])))
                    self.__students_table.setItem(row_no, 5, QTableWidgetItem(str(row_data["status"])))
                    self.__students_table.setItem(row_no, 6, QTableWidgetItem(str(row_data["registered_on"])))
                    self.__students_table.setItem(row_no, 7, QTableWidgetItem(str(row_data["expiry_date"])))
                    self.__students_table.setRowCount(len(students_docs))

    def setup_header(self) -> NoReturn:
        header_title = QLabel()
        header_title.setText("Students")
        header_title.setStyleSheet(
            """
            color: black;
            font-size: 20px;
            """
        )

        page_title = QLabel()
        page_title.setText("Dashboard/Students")
        page_title.setStyleSheet(
            """
            color: black;
            font-size: 12px;
            """
        )

        self.__header.addWidget(header_title)
        self.__header.addStretch(1)
        self.__header.addWidget(page_title)

    def add_header_to_container(self) -> NoReturn:
        self.__container.addRow(self.__header)

    def add_statistics_to_container(self) -> NoReturn:
        self.__container.addRow(self.__statistics)

    def add_searchbar_to_container(self) -> NoReturn:
        self.__container.addRow(self.__searchbar)

    def add_students_table_to_container(self) -> NoReturn:
        self.__container.addRow(self.__students_table)

    def add_frame_to_main_layout(self) -> NoReturn:
        self.__main_layout.addWidget(self.__frame)

    def show_add_student_dialog(self) -> NoReturn:
        add_student_dialog = AddStudentsForm()
        add_student_dialog.exec()

    def load_ui(self) -> NoReturn:
        self.init_frame()
        self.init_header()
        self.init_container()
        self.init_searchbar()
        self.init_main_layout()
        self.init_statistics()
        self.init_search_input()
        self.init_students_table()
        self.init_all_students_count()
        self.init_active_students_count()
        self.init_pending_students_count()
        self.init_deactivated_students_count()

        self.setup_main_layout()
        self.setup_frame()
        self.setup_container()
        self.setup_header()
        self.setup_statistics()
        self.setup_search_input()
        self.setup_searchbar()
        self.setup_students_table()

        self.add_frame_to_main_layout()
        self.add_header_to_container()
        self.add_statistics_to_container()
        self.add_searchbar_to_container()
        self.add_students_table_to_container()


if __name__ == "__main__":
    from sys import argv

    app = QApplication(argv)
    window = StudentsPage()
    window.show()
    app.exec_()
