from collections import defaultdict
from itertools import repeat
from typing import NoReturn

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations


class SettingsPage(QWidget, RethinkDBOperations):
    def __init__(self):
        QWidget.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)

        self.__frame, \
        self.__header, \
        self.__container, \
        self.__main_layout, \
        self.__form_widget, \
        self.__form_layout, \
        self.__tree_widget, \
        self.__holder_layout = repeat(None, 8)

        self.load_ui()

    def init_frame(self) -> NoReturn:
        self.__frame = QFrame(self)

    def init_header(self) -> NoReturn:
        self.__header = QHBoxLayout()

    def init_tree_widget(self) -> NoReturn:
        self.__tree_widget = QTreeWidget()

    def init_container(self) -> NoReturn:
        self.__container = QFormLayout()

    def init_main_layout(self) -> NoReturn:
        self.__main_layout = QVBoxLayout()

    def init_holder_layout(self) -> NoReturn:
        self.__holder_layout = QHBoxLayout()

    def init_form_widget(self) -> NoReturn:
        self.__form_widget = QWidget()

    def init_form_layout(self) -> NoReturn:
        self.__form_layout = QVBoxLayout()

    def setup_tree_widget(self) -> NoReturn:

        self.__tree_widget.setHeaderLabels(["Audit_Trail", "Audit Type"])
        self.__tree_widget.setColumnCount(2)
        self.__tree_widget.setColumnWidth(0, 700)

        self.__tree_widget.setAlternatingRowColors(True)
        audit_logs_result = defaultdict(list)

        audit_logs_docs = self.table_docs(BaseConfig.db, BaseConfig.audits_table)

        if isinstance(audit_logs_docs, dict):
            QMessageBox.critical(self, "Critical", audit_logs_docs["msg"])
        elif isinstance(audit_logs_docs, list):
            if not audit_logs_docs:
                pass
            else:
                for log in audit_logs_docs:
                    if log["date_added"]:
                        audit_logs_result[log["date_added"]].append([log["audit_trails"], log["audit_type"]])

                for k, v in audit_logs_result.items():
                    top_level_item = QTreeWidgetItem(self.__tree_widget, [k])
                    top_level_item.setForeground(0, QBrush(QColor("black")))
                    top_level_item.setIcon(0, QIcon("../icons/question1.png"))

                    v.reverse()

                    for i in v:
                        if len(i) == 2:
                            sub_level_item = QTreeWidgetItem(top_level_item)
                            sub_level_item.setForeground(0, QBrush(QColor("black")))
                            sub_level_item.setForeground(1, QBrush(QColor("black")))
                            sub_level_item.setIcon(0, QIcon("../icons/alert2.png"))
                            sub_level_item.setText(0, f"{i[0]}")
                            if i[1] == "failed_login":
                                sub_level_item.setIcon(1, QIcon("../icons/alert1.png"))
                                sub_level_item.setText(1, f"{i[1]}")
                            elif i[1] == "login":
                                sub_level_item.setIcon(1, QIcon("../icons/logged_in1.png"))
                                sub_level_item.setText(1, f"{i[1]}")
                            elif i[1] == "logout":
                                sub_level_item.setIcon(1, QIcon("../icons/logout_icon.png"))
                                sub_level_item.setText(1, f"{i[1]}")
                            elif i[1] == "add":
                                sub_level_item.setIcon(1, QIcon("../icons/student_added1.png"))
                                sub_level_item.setText(1, f"{i[1]}")
                            elif i[1] == "edit":
                                sub_level_item.setIcon(1, QIcon("../icons/student_edited1.png"))
                                sub_level_item.setText(1, f"{i[1]}")

    def setup_form_widget(self) -> NoReturn:
        self.__form_widget.setFixedWidth(200)
        self.__form_widget.setStyleSheet(
            """
            background-color: red;
            """
        )
        self.__form_widget.setLayout(self.__form_layout)

    def setup_form_layout(self) -> NoReturn:
        self.__form_layout.setContentsMargins(0, 0, 0, 0)
        self.__form_layout.setAlignment(Qt.AlignTop)

    def setup_main_layout(self):
        # self.setFixedSize(QSize(1000, 700))
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
                QLineEdit {
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

    def setup_holder_layout(self) -> NoReturn:
        self.__holder_layout.setContentsMargins(0, 0, 0, 0)

    def setup_header(self) -> NoReturn:
        header_title = QLabel()
        header_title.setText("Settings")
        header_title.setStyleSheet(
            """
            color: black;
            font-size: 20px;
            """
        )

        page_title = QLabel()
        page_title.setText("Dashboard/Settings")
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

    def add_holder_layout_to_container(self) -> NoReturn:
        self.__container.addRow(self.__holder_layout)

    def add_frame_to_main_layout(self) -> NoReturn:
        self.__main_layout.addWidget(self.__frame)

    def add_form_widget_to_holder_layout(self) -> NoReturn:
        self.__holder_layout.addWidget(self.__form_widget)

    def add_tree_widget_to_holder_layout(self) -> NoReturn:
        self.__holder_layout.addWidget(self.__tree_widget)

    def load_ui(self) -> NoReturn:
        self.init_frame()
        self.init_header()
        self.init_container()
        self.init_main_layout()
        self.init_holder_layout()
        self.init_form_widget()
        self.init_form_layout()
        self.init_tree_widget()

        self.setup_main_layout()
        self.setup_frame()
        self.setup_container()
        self.setup_header()
        self.setup_holder_layout()
        self.setup_form_widget()
        self.setup_form_layout()
        self.setup_tree_widget()

        self.add_frame_to_main_layout()
        self.add_header_to_container()
        self.add_holder_layout_to_container()
        # self.add_form_widget_to_holder_layout()
        self.add_tree_widget_to_holder_layout()


if __name__ == "__main__":
    from sys import argv

    app = QApplication(argv)
    window = SettingsPage()
    window.show()
    app.exec_()
