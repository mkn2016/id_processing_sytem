from datetime import datetime
from typing import NoReturn

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations


class BranchesPage(QWidget, RethinkDBOperations):
    def __init__(self):
        QWidget.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)

        self.__item_id,\
        self.__form_widget,\
        self.__button_widget,\
        self.__button_layout,\
        self.__form_layout,\
        self.__table,\
        self.__frame,\
        self.__header,\
        self.__container,\
        self.__main_layout,\
        self.__holder_layout,\
        self.__title,\
        self.__submit_btn,\
        self.__cancel_btn = [None for _ in range(14)]
        self.__edit_event = False
        self.__add_event = True

        self.load_ui()

    def init_submit_btn(self) -> NoReturn:
        self.__submit_btn = QPushButton()

    def init_form_layout(self) -> NoReturn:
        self.__form_layout = QVBoxLayout()

    def init_cancel_btn(self) -> NoReturn:
        self.__cancel_btn = QPushButton()

    def init_button_widget(self) -> NoReturn:
        self.__button_widget = QWidget()

    def init_button_layout(self) -> NoReturn:
        self.__button_layout = QHBoxLayout()

    def init_title(self) -> NoReturn:
        self.__title = QLineEdit()

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
        header_title.setText("Branches")
        header_title.setStyleSheet(
            """
            color: black;
            font-size: 20px;
            """
        )

        page_title = QLabel()
        page_title.setText("Dashboard/Branches")
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
        self.__table.setColumnCount(4)
        self.__table.setAlternatingRowColors(True)

        self.__table.setStyleSheet(
            """
            QTableWidget{
                color: black;
            }
            """
        )

        self.__table.setColumnWidth(0, 150)
        self.__table.setColumnWidth(1, 200)
        self.__table.setColumnWidth(2, 250)
        self.__table.setColumnWidth(3, 200)

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
            ("", "", "", ""))

        id_ = self.__table.horizontalHeaderItem(0)
        id_.setIcon(QIcon("../icons/id1.png"))
        id_.setText("Id No")

        title = self.__table.horizontalHeaderItem(1)
        title.setIcon(QIcon("../icons/title.png"))
        title.setText("Title")

        date_created = self.__table.horizontalHeaderItem(2)
        date_created.setIcon(QIcon("../icons/year_added.png"))
        date_created.setText("Date Created")

        date_modified = self.__table.horizontalHeaderItem(3)
        date_modified.setIcon(QIcon("../icons/year_expiring.png"))
        date_modified.setText("Date Modified")

    def setup_form_layout(self) -> NoReturn:
        self.__form_layout.setContentsMargins(0, 0, 0, 0)
        self.__form_layout.setAlignment(Qt.AlignTop)

    def setup_title(self) -> NoReturn:
        self.__title.setContentsMargins(0, 0, 0, 0)
        self.__title.setPlaceholderText("Enter Branch Title")
        self.__title.setStyleSheet(
            """
            color: black
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
        self.__button_widget.setContentsMargins(0,0,0,0)
        self.__button_widget.setLayout(self.__button_layout)

    def setup_button_layout(self) -> NoReturn:
        self.__button_layout.setContentsMargins(0,0,0,0)

    def showEvent(self, e) -> NoReturn:
        self.load_branches_table_data()

    def enterEvent(self, e) -> NoReturn:
        self.load_branches_table_data()

    def load_branches_table_data(self) -> NoReturn:
        branches_docs = self.table_docs(BaseConfig.db, BaseConfig.branches_table)

        if isinstance(branches_docs, dict):
            QMessageBox.critical(self, "Critical", branches_docs["msg"])
        elif isinstance(branches_docs, list):
            if not branches_docs:
                pass
            else:
                self.__table.clearContents()
                self.__table.setRowCount(0)

                for row_no, row_data in enumerate(branches_docs):
                    self.__table.insertRow(row_no)

                    id_item = QTableWidgetItem(str(row_data["id"]))
                    title_item = QTableWidgetItem(str(row_data["title"]))
                    date_created_item = QTableWidgetItem(str(row_data["date_created"]))
                    date_modified_item = QTableWidgetItem(str(row_data["date_modified"]))

                    self.__table.setItem(row_no, 0, id_item)
                    self.__table.setItem(row_no, 1, title_item)
                    self.__table.setItem(row_no, 2, date_created_item)
                    self.__table.setItem(row_no, 3, date_modified_item)

                    self.__table.setRowCount(len(branches_docs))
                self.__table.clicked.connect(self.on_cell_click)

    def on_cell_click(self) -> NoReturn:
        index = self.__table.selectionModel().currentIndex()
        id_value = index.siblingAtColumn(0)
        title_value = index.siblingAtColumn(1)
        self.__item_id = id_value.data()
        self.__title.setText(title_value.data())
        self.__edit_event = True
        self.__add_event = False

    def on_submit(self) -> NoReturn:
        if self.__edit_event:

            title = self.__title.text()

            if not title:
                QMessageBox.critical(self, "Critical", "Title can not be empty")
                self.reset()
            else:
                doc = self.get_doc_by_id(BaseConfig.db, BaseConfig.branches_table, int(self.__item_id))

                if title == doc["result"]["title"]:
                    QMessageBox.critical(self, "Critical",
                                         "Title is the same as the one in the database. Skipping editing.")
                else:
                    branch_id = doc["result"]["id"]

                    branch_doc = {
                        "title": title,
                        "date_modified": datetime.today().strftime("%d-%m-%Y %H:%M:%S")
                    }

                    doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.branches_table, branch_doc,
                                                        branch_id)
                    if doc_update_result["result"]:
                        QMessageBox.information(self, "Success", "Branch updated successfully")
                        self.reset()
                    else:
                        QMessageBox.critical(self, "Critical", doc_update_result["msg"])
                        self.reset()
        elif self.__add_event:
            title = self.__title.text()

            if not title:
                QMessageBox.critical(self, "Critical", "Title can not be empty")
            else:
                print(title)
                id_result = self.generate_id(BaseConfig.db, BaseConfig.branches_table)

                if id_result["result"] is None:
                    QMessageBox.critical(self, "Critical", id_result["msg"])
                else:
                    branch_doc = {
                        "id": id_result["result"],
                        "title": title,
                        "date_created": datetime.today().strftime("%d-%m-%Y %H:%M:%S"),
                        "date_modified": datetime.today().strftime("%d-%m-%Y %H:%M:%S")

                    }

                    doc_insert_result = self.insert_doc_to_table(BaseConfig.db, BaseConfig.branches_table, branch_doc)

                    if doc_insert_result["result"]:
                        QMessageBox.information(self, "Success", "Branch inserted successfully")
                        self.__title.clear()
                    else:
                        QMessageBox.critical(self, "Critical", doc_insert_result["msg"])
                        self.__title.clear()

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

    def add_button_widget_to_form_layout(self) -> NoReturn:
        self.__form_layout.addWidget(self.__button_widget)

    def add_cancel_btn_to_button_layout(self) -> NoReturn:
        self.__button_layout.addWidget(self.__cancel_btn)

    def add_submit_btn_to_button_layout(self) -> NoReturn:
        self.__button_layout.addWidget(self.__submit_btn)

    def reset(self) -> NoReturn:
        self.__title.clear()
        self.__add_event = True
        self.__edit_event = False

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
        self.init_button_layout()
        self.init_cancel_btn()
        self.init_button_widget()

        self.setup_main_layout()
        self.setup_frame()
        self.setup_container()
        self.setup_header()
        self.setup_holder_layout()
        self.setup_form_widget()
        self.setup_form_layout()
        self.setup_title()
        self.setup_button_widget()
        self.setup_button_layout()
        self.setup_submit_btn()
        self.setup_cancel_btn()
        self.setup_table()

        self.add_frame_to_main_layout()
        self.add_header_to_container()
        self.add_holder_layout_to_container()
        self.add_form_widget_to_holder_layout()
        self.add_title_to_form_layout()
        self.add_button_widget_to_form_layout()
        self.add_cancel_btn_to_button_layout()
        self.add_submit_btn_to_button_layout()
        self.add_table_to_holder_layout()