from typing import NoReturn
from datetime import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations
from src.views.courses import degree_programmes, masters_programmes, doctors_programmes


class CoursesPage(QWidget, RethinkDBOperations):
    def __init__(self):
        QWidget.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)

        self.__form_widget = None
        self.__form_layout = None
        self.__table = None
        self.__frame = None
        self.__header = None
        self.__container = None
        self.__main_layout = None
        self.__holder_layout = None
        self.__title = None
        self.__level = None
        self.__abbreviation = None
        self.__submit_btn = None
        self.__item_id = None
        self.__button_widget = None
        self.__button_layout = None
        self.__cancel_btn = None
        self.__edit_event = False
        self.__add_event = True

        self.load_ui()

    def init_submit_btn(self) -> NoReturn:
        self.__submit_btn = QPushButton()

    def init_form_layout(self) -> NoReturn:
        self.__form_layout = QVBoxLayout()

    def init_title(self) -> NoReturn:
        self.__title = QLineEdit()

    def init_level(self) -> NoReturn:
        self.__level = QComboBox()

    def init_cancel_btn(self) -> NoReturn:
        self.__cancel_btn = QPushButton()

    def init_button_widget(self) -> NoReturn:
        self.__button_widget = QWidget()

    def init_button_layout(self) -> NoReturn:
        self.__button_layout = QHBoxLayout()

    def init_abbreviation(self) -> NoReturn:
        self.__abbreviation = QComboBox()

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
        self.load_courses_table_data()

    def enterEvent(self, e) -> NoReturn:
        self.load_courses_table_data()

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
        header_title.setText("Courses")
        header_title.setStyleSheet(
            """
            color: black;
            font-size: 20px;
            """
        )

        page_title = QLabel()
        page_title.setText("Dashboard/Courses")
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
        self.__table.setColumnCount(7)
        self.__table.setAlternatingRowColors(True)

        self.__table.setStyleSheet(
            """
            QTableWidget{
                color: black;
            }
            """
        )

        self.__table.setColumnWidth(0, 100)
        self.__table.setColumnWidth(1, 150)
        self.__table.setColumnWidth(2, 100)
        self.__table.setColumnWidth(3, 150)
        self.__table.setColumnWidth(4, 250)
        self.__table.setColumnWidth(5, 200)
        self.__table.setColumnWidth(6, 200)

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
            ("", "", "", "", "", "", ""))

        id_ = self.__table.horizontalHeaderItem(0)
        id_.setIcon(QIcon("../icons/id1.png"))
        id_.setText("Id No")

        level = self.__table.horizontalHeaderItem(1)
        level.setIcon(QIcon("../icons/name.png"))
        level.setText("Level")

        abbreviation = self.__table.horizontalHeaderItem(2)
        abbreviation.setIcon(QIcon("../icons/name.png"))
        abbreviation.setText("Abbreviation")

        title = self.__table.horizontalHeaderItem(3)
        title.setIcon(QIcon("../icons/title.png"))
        title.setText("Title")

        course_title = self.__table.horizontalHeaderItem(4)
        course_title.setIcon(QIcon("../icons/title.png"))
        course_title.setText("Course_Title")

        date_created = self.__table.horizontalHeaderItem(5)
        date_created.setIcon(QIcon("../icons/year_added.png"))
        date_created.setText("Date Created")

        date_modified = self.__table.horizontalHeaderItem(6)
        date_modified.setIcon(QIcon("../icons/year_expiring.png"))
        date_modified.setText("Date Modified")

    def setup_form_layout(self) -> NoReturn:
        self.__form_layout.setContentsMargins(0, 0, 0, 0)
        self.__form_layout.setAlignment(Qt.AlignTop)

    def setup_title(self) -> NoReturn:
        self.__title.setContentsMargins(0, 0, 0, 0)
        self.__title.setPlaceholderText("Enter Course Title")
        self.__title.setStyleSheet(
            """
            color: black
            """
        )

    def setup_level(self) -> NoReturn:
        self.__level.setFixedHeight(25)
        self.__level.setContentsMargins(0, 0, 0, 0)
        self.__level.addItems([
            "Certificate",
            "Diploma",
            "Degree",
            "Postgraduate Diploma",
            "Masters",
            "Doctorate"
        ])
        self.__level.setCurrentText("Degree")
        self.__level.setStyleSheet(
            """
            border-radius: 1;
            color: black;
            border: 1px solid black;
            """
        )
        self.__level.setDuplicatesEnabled(False)
        self.__level.currentTextChanged.connect(self.on_current_text_changed)

    def on_current_text_changed(self, arg1) -> NoReturn:
        print(arg1)
        print(self.__add_event)
        print(self.__edit_event)
        if self.__edit_event:
            if arg1 == "Degree":
                self.__abbreviation.insertItems(0, degree_programmes)
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(len(degree_programmes))
                self.__abbreviation.setCurrentText("BA.")
            elif arg1 == "Diploma":
                self.__abbreviation.insertItem(0, "Dip.")
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(1)
                self.__abbreviation.setCurrentText("Dip.")
            elif arg1 == "Certificate":
                self.__abbreviation.insertItem(0, "Cert.")
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(1)
                self.__abbreviation.setCurrentText("Cert.")
            elif arg1 == "Postgraduate Diploma":
                self.__abbreviation.insertItem(0, "PgDip.")
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(1)
                self.__abbreviation.setCurrentText("PgDip.")
            elif arg1 == "Masters":
                self.__abbreviation.insertItems(0, masters_programmes)
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(len(masters_programmes))
                self.__abbreviation.setCurrentText("M.A.")
            elif arg1 == "Doctorate":
                self.__abbreviation.insertItems(0, doctors_programmes)
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(len(doctors_programmes))
                self.__abbreviation.setCurrentText("PhD.")
        elif self.__add_event:
            if arg1 == "Degree":
                self.__abbreviation.insertItems(0, degree_programmes)
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(len(degree_programmes))
                self.__abbreviation.setCurrentText("BA.")
            elif arg1 == "Diploma":
                self.__abbreviation.insertItem(0, "Dip.")
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(1)
                self.__abbreviation.setCurrentText("Dip.")
            elif arg1 == "Certificate":
                self.__abbreviation.insertItem(0, "Cert.")
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(1)
                self.__abbreviation.setCurrentText("Cert.")
            elif arg1 == "Postgraduate Diploma":
                self.__abbreviation.insertItem(0, "PgDip.")
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(1)
                self.__abbreviation.setCurrentText("PgDip.")
            elif arg1 == "Masters":
                self.__abbreviation.insertItems(0, masters_programmes)
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(len(masters_programmes))
                self.__abbreviation.setCurrentText("M.A.")
            elif arg1 == "Doctorate":
                self.__abbreviation.insertItems(0, doctors_programmes)
                self.__abbreviation.setInsertPolicy(QComboBox.InsertAtCurrent)
                self.__abbreviation.setMaxCount(len(doctors_programmes))
                self.__abbreviation.setCurrentText("PhD.")

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
        self.__button_widget.setContentsMargins(0,0,0,0)
        self.__button_widget.setLayout(self.__button_layout)

    def setup_button_layout(self) -> NoReturn:
        self.__button_layout.setContentsMargins(0,0,0,0)

    def on_submit(self) -> NoReturn:
        if self.__edit_event:
            title = self.__title.text()
            level = self.__level.currentText()
            abbreviation = self.__abbreviation.currentText()

            if not title:
                QMessageBox.critical(self, "Critical", "Title can not be empty.")
                self.reset()
            else:
                doc = self.get_doc_by_id(BaseConfig.db, BaseConfig.courses_table, int(self.__item_id))

                if title == doc["result"]["title"] and level == doc["result"]["level"] and abbreviation == doc["result"]["abbreviation"]:
                    QMessageBox.critical(self, "Critical",
                                         "Item in database is the same as the inputs. Nothing to update. Skipping editing.")
                else:
                    course_id = doc["result"]["id"]

                    course_doc = {
                        "level": level,
                        "abbreviation": abbreviation,
                        "title": title,
                        "course_title": self.__abbreviation.currentText()+title,
                        "date_modified": datetime.today().strftime("%d-%m-%Y %H:%M:%S")
                    }

                    doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.courses_table, course_doc,
                                                        course_id)
                    if doc_update_result["result"]:
                        QMessageBox.information(self, "Success", "department updated successfully")
                        self.reset()
                    else:
                        QMessageBox.critical(self, "Critical", doc_update_result["msg"])
                        self.reset()
        elif self.__add_event:
            title = self.__title.text()

            if not title:
                QMessageBox.critical(self, "Critical", "Title can not be empty")
            else:
                id_result = self.generate_id(BaseConfig.db, BaseConfig.courses_table)

                if id_result["result"] is None:
                    QMessageBox.critical(self, "Critical", id_result["msg"])
                else:
                    course_doc = {
                        "id": id_result["result"],
                        "title": title,
                        "level": self.__level.currentText(),
                        "abbreviation": self.__abbreviation.currentText(),
                        "course_title": self.__abbreviation.currentText()+title,
                        "date_created": datetime.today().strftime("%d-%m-%Y %H:%M:%S"),
                        "date_modified": datetime.today().strftime("%d-%m-%Y %H:%M:%S")

                    }

                    doc_insert_result = self.insert_doc_to_table(BaseConfig.db, BaseConfig.courses_table, course_doc)

                    if doc_insert_result["result"]:
                        QMessageBox.information(self, "Success", "Course inserted successfully")
                        self.reset()
                    else:
                        QMessageBox.critical(self, "Critical", doc_insert_result["msg"])
                        self.reset()

    def load_courses_table_data(self) -> NoReturn:
        courses_docs = self.table_docs(BaseConfig.db, BaseConfig.courses_table)

        if isinstance(courses_docs, dict):
            QMessageBox.critical(self, "Critical", courses_docs["msg"])
        elif isinstance(courses_docs, list):
            if not courses_docs:
                pass
            else:
                self.__table.clearContents()
                self.__table.setRowCount(0)

                for row_no, row_data in enumerate(courses_docs):
                    self.__table.insertRow(row_no)

                    id_item = QTableWidgetItem(str(row_data["id"]))
                    level_item = QTableWidgetItem(str(row_data["level"]))
                    abbreviation_item = QTableWidgetItem(str(row_data["abbreviation"]))
                    title_item = QTableWidgetItem(str(row_data["title"]))
                    course_title_item = QTableWidgetItem(str(row_data["course_title"]))
                    date_created_item = QTableWidgetItem(str(row_data["date_created"]))
                    date_modified_item = QTableWidgetItem(str(row_data["date_modified"]))

                    self.__table.setItem(row_no, 0, id_item)
                    self.__table.setItem(row_no, 1, level_item)
                    self.__table.setItem(row_no, 2, abbreviation_item)
                    self.__table.setItem(row_no, 3, title_item)
                    self.__table.setItem(row_no, 4, course_title_item)
                    self.__table.setItem(row_no, 5, date_created_item)
                    self.__table.setItem(row_no, 6, date_modified_item)

                    self.__table.setRowCount(len(courses_docs))
                self.__table.clicked.connect(self.on_cell_click)

    def on_cell_click(self) -> NoReturn:
        index = self.__table.selectionModel().currentIndex()
        id_value = index.siblingAtColumn(0)
        level_value = index.siblingAtColumn(1)
        abbreviation_value = index.siblingAtColumn(2)
        title_value = index.siblingAtColumn(3)

        self.__item_id = id_value.data()
        self.__title.setText(title_value.data())
        self.__level.setCurrentText(level_value.data())
        self.__abbreviation.setCurrentText(abbreviation_value.data())

        self.__edit_event = True
        self.__add_event = False

    def reset(self) -> NoReturn:
        self.__title.clear()
        self.__title.clear()
        self.__add_event = True
        self.__edit_event = False
        self.__level.setCurrentText("Degree")
        self.__abbreviation.setCurrentText("BA.")

    def setup_abbreviation(self) -> NoReturn:
        self.__abbreviation.setFixedHeight(25)
        self.__abbreviation.setContentsMargins(0, 0, 0, 0)
        self.__abbreviation.setStyleSheet(
            """
            border-radius: 1;
            color: black;
            border: 1px solid black;
            """
        )
        self.__abbreviation.addItems(degree_programmes)
        self.__abbreviation.setCurrentText("B.A.")
        if self.__add_event:
            self.__abbreviation.addItems(degree_programmes)
            self.__abbreviation.setCurrentText("B.A.")
        elif self.__edit_event:
            self.__abbreviation.addItems([])
            self.__abbreviation.setCurrentText("")

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

    def add_title_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__title)

    def add_level_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__level)

    def add_abbreviation_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__abbreviation)

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
        self.init_title()
        self.init_submit_btn()
        self.init_level()
        self.init_abbreviation()
        self.init_cancel_btn()
        self.init_button_layout()
        self.init_button_widget()

        self.setup_main_layout()
        self.setup_frame()
        self.setup_container()
        self.setup_header()
        self.setup_holder_layout()
        self.setup_form_widget()
        self.setup_form_layout()
        self.setup_level()
        self.setup_abbreviation()
        self.setup_title()
        self.setup_submit_btn()
        self.setup_cancel_btn()
        self.setup_button_layout()
        self.setup_button_widget()
        self.setup_table()

        self.add_frame_to_main_layout()
        self.add_header_to_container()
        self.add_holder_layout_to_container()
        self.add_form_widget_to_holder_layout()
        self.add_level_to_form_layout()
        self.add_abbreviation_to_form_layout()
        self.add_title_to_form_layout()
        self.add_button_widget_to_form_layout()
        self.add_cancel_btn_to_button_layout()
        self.add_submit_btn_to_button_layout()
        self.add_table_to_holder_layout()
