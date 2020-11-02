from typing import NoReturn

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from src.config.config import BaseConfig

from src.views.courses.courses import CoursesPage
from src.views.branches.branches import BranchesPage
from src.views.students.students import StudentsPage
from src.views.employees.employees import EmployeesPage
from src.views.settings.settings import SettingsPage
from src.utils.audit.audit_trails import parse_audit_logs
from src.views.departments.departments import DepartmentsPage
from src.db.operations.db_operations import RethinkDBOperations


class MainWindow(QMainWindow, RethinkDBOperations):
    switch_window = pyqtSignal()

    def __init__(self, settings=None):
        QMainWindow.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)
        self.menu, \
        self.toolbar, \
        self.tab_widget, \
        self.main_layout, \
        self.corner_tab, \
        self.time_display = [None for _ in range(6)]
        self.settings = settings
        self.username = None
        self.full_name = None
        self.role = None
        self.username1 = None

        QMainWindow.__init__(self)

        self.load_ui()

    def initialize_time_display(self):
        self.time_display = QLabel("--:--:--")
        self.time_display.setStyleSheet(
            """
            font-size: 12px;
            color: black;
            """
        )

    def init_fullname(self):
        self.full_name = QLabel()

    def initialize_toolbar(self):
        self.toolbar = QToolBar()

    def initialize_layout(self):
        self.main_layout = QVBoxLayout()

    def initialize_tabs(self):
        self.tab_widget = QTabWidget()
        stylesheet = """ 
            QTabWidget::pane { /* The tab widget frame */
                border-top: 1px solid #C2C7CB;
            }

            QTabWidget::tab-bar {
                left: 20px; /* move to the right by 20px */
            }

            /* Style the tab using the tab sub-control. Note that
                it reads QTabBar _not_ QTabWidget */
            QTabBar::tab {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #E1E1E1, stop: 0.4 #DDDDDD,
                                            stop: 0.5 #D8D8D8, stop: 1.0 #D3D3D3);
                border: 2px solid #C4C4C3;
                border-bottom-color: #C2C7CB; /* same as the pane color */
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                min-width: 12ex;
                min-height: 6ex
            }

            QTabBar::tab:selected, QTabBar::tab:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                            stop: 0 #fafafa, stop: 0.4 #f4f4f4,
                                            stop: 0.5 #e7e7e7, stop: 1.0 #fafafa);
            }

            QTabBar::tab:selected {
                border-color: teal;
                border-bottom-color: #C2C7CB; /* same as pane color */
            }

            QTabBar::tab:!selected {
                margin-top: 2px; /* make non-selected tabs look smaller */
            }

            /* make use of negative margins for overlapping tabs */
            QTabBar::tab:selected {
                /* expand/overlap to the left and right by 4px */
                margin-left: -4px;
                margin-right: -4px;
            }

            QTabBar::tab:first:selected {
                margin-left: 0; /* the first selected tab has nothing to overlap with on the left */
            }

            QTabBar::tab:last:selected {
                margin-right: 0; /* the last selected tab has nothing to overlap with on the right */
            }

            QTabBar::tab:only-one {
                margin: 0; /* if there is only one tab, we don't want overlapping margins */
            }
        """
        self.tab_widget.setStyleSheet(stylesheet)

    def setup_full_name(self):
        self.full_name.setStyleSheet(
            """
            color: black;
            font-size: 14px
            """
        )
        self.full_name.setText(self.username)

    def add_corner_tabs(self):
        corner_widget = QWidget()

        corner_layout = QHBoxLayout()

        logout_btn = QPushButton("Logout")
        logout_btn.setFlat(True)
        logout_btn.setIcon(QIcon("../icons/logout2.png"))
        logout_btn.clicked.connect(self.on_logout)

        shutdown_btn = QPushButton("Shutdown")
        shutdown_btn.setFlat(True)
        shutdown_btn.setIcon(QIcon("../icons/shutdown1.png"))
        shutdown_btn.clicked.connect(self.on_shutdown)

        corner_layout.addWidget(logout_btn)
        corner_layout.addWidget(shutdown_btn)

        corner_widget.setLayout(corner_layout)

        self.tab_widget.setCornerWidget(corner_widget, Qt.TopRightCorner)

    def add_tabs(self) -> NoReturn:
        self.tab_widget.addTab(StudentsPage(), QIcon("../icons/stud1.png"), "Students")
        self.tab_widget.addTab(EmployeesPage(), QIcon("../icons/emp1.png"), "Employees")
        self.tab_widget.addTab(DepartmentsPage(), QIcon("../icons/dep1.png"), "Departments")
        self.tab_widget.addTab(BranchesPage(), QIcon("../icons/location1.png"), "Branches")
        self.tab_widget.addTab(CoursesPage(), QIcon("../icons/course.png"), "Courses")
        self.tab_widget.addTab(SettingsPage(), QIcon("../icons/settings1.png"), "Settings")

    def add_tool_bar(self) -> NoReturn:

        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet(
            "background-color: transparent;"
            "font-size: 24;"
            "color: black;"
        )

        toolbar_widget = QWidget()
        toolbar_layout = QHBoxLayout()

        timer = QTimer(self)
        try:
            timer.timeout.connect(self.show_time)
        except KeyboardInterrupt:
            pass
        else:
            timer.start(1000)

        online_widget = QWidget()
        online_widget.setFixedSize(QSize(400, 40))
        online_layout = QHBoxLayout()
        online_layout.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)

        online_icon = QLabel()
        online_icon.setPixmap(QPixmap("../icons/online3.png"))

        online_layout.addWidget(online_icon)
        online_layout.addWidget(self.full_name)

        online_widget.setLayout(online_layout)

        last_login_and_time = QWidget()
        last_login_and_time_layout = QHBoxLayout()

        last_login_text = QLabel()
        last_login_text.setStyleSheet(
            """
            color: black;
            font-size: 14px
            """
        )
        last_login_text.setText("Last logged in: ")

        current_date = QLabel()
        current_date.setStyleSheet(
            """
            color: black;
            font-size: 14px
            """
        )
        current_date.setText("date")

        last_login_and_time_layout.addWidget(last_login_text)
        last_login_and_time_layout.addWidget(current_date)
        last_login_and_time_layout.addWidget(self.time_display)

        last_login_and_time.setLayout(last_login_and_time_layout)

        toolbar_layout.addWidget(online_widget)
        toolbar_layout.addStretch(1)
        toolbar_layout.addWidget(last_login_and_time)

        toolbar_widget.setLayout(toolbar_layout)

        self.toolbar.addWidget(toolbar_widget)

        self.addToolBar(self.toolbar)

    def paintEvent(self, paintRect):
        self.username = self.settings.value("name")
        self.role = self.settings.value("role")

    def showEvent(self, e) -> NoReturn:
        self.username = self.settings.value("name")
        self.role = self.settings.value("role")

        self.full_name.setText(self.username)

    def enterEvent(self, e) -> NoReturn:
        self.username = self.settings.value("name")
        self.role = self.settings.value("role")

    def set_tabs_to_layout(self) -> NoReturn:
        self.main_layout.addWidget(self.tab_widget)

    def show_time(self):
        time = QTime.currentTime()
        time_string = time.toString("hh:mm:ss")
        self.time_display.setText(time_string)

    def init_main(self) -> NoReturn:
        self.statusBar().showMessage("Ready")
        self.setWindowTitle("Student ID Processing System")
        w = QWidget(self)
        self.setCentralWidget(w)
        w.setLayout(self.main_layout)
        self.setStyleSheet(
           """
           """
        )

    @pyqtSlot(str, str)
    def on_submitted(self, name, role):
        pass

    def on_logout(self) -> NoReturn:
        audit_log_id = self.generate_id(BaseConfig.db, "audit_trails")

        audit_log = parse_audit_logs(audit_log_id["result"], self.username, "logout")

        audit_log_result = self.insert_doc_to_table(BaseConfig.db, "audit_trails", audit_log)
        if audit_log_result["result"] is None:
            pass
        self.switch_window.emit()

    def on_shutdown(self):
        choice = QMessageBox.question(
            self,
            "Exiting...",
            "Are you sure you want to Exit?",
            QMessageBox.Yes | QMessageBox.No
        )
        if choice == QMessageBox.Yes:
            qApp.closeAllWindows()
        else:
            self.setFocus()

    def load_ui(self) -> NoReturn:
        self.init_fullname()
        self.initialize_time_display()
        self.initialize_toolbar()
        self.initialize_layout()
        self.initialize_tabs()
        self.setup_full_name()
        self.add_tabs()
        self.add_corner_tabs()
        self.add_tool_bar()
        self.set_tabs_to_layout()
        self.init_main()


if __name__ == "__main__":
    from sys import argv

    app = QApplication(argv)
    window = MainWindow()
    window.show()
    app.exec_()