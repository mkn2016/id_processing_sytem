from datetime import datetime
from itertools import repeat
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import NoReturn

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from rethinkdb import r

from src.config.config import BaseConfig
from src.db.operations.db_operations import RethinkDBOperations
from src.utils.messenger.message_parser import Messenger
from src.utils.qrcode.qrcode_encoder import encode_data_to_file
from src.utils.sms.sms import AfricasTalkingSMS
from src.views.students import end_dated


class EditStudentsForm(QDialog, RethinkDBOperations, AfricasTalkingSMS):
    def __init__(self):
        QDialog.__init__(self)
        RethinkDBOperations.__init__(self, **BaseConfig.dbcon)
        AfricasTalkingSMS.__init__(self)

        self.__tel, \
        self.__zip, \
        self.__city, \
        self.__email, \
        self.__state, \
        self.__course, \
        self.__branch, \
        self.__status, \
        self.__country, \
        self.__country, \
        self.__surname, \
        self.__save_btn, \
        self.__address1, \
        self.__male, \
        self.__female, \
        self.__tel_email_errors_widget, \
        self.__tel_email_errors_layout, \
        self.__tel_error_label, \
        self.__email_error_label, \
        self.__address2, \
        self.__dob_label, \
        self.__first_name, \
        self.__dob_layout, \
        self.__dob_widget, \
        self.__department, \
        self.__middle_name, \
        self.__id_passport, \
        self.__main_layout, \
        self.__main_layout, \
        self.__day_combobox, \
        self.__names_widget, \
        self.__names_layout, \
        self.__status_widget, \
        self.__status_layout, \
        self.__gender_widget, \
        self.__gender_layout, \
        self.__year_combobox, \
        self.__address_widget, \
        self.__address_layout, \
        self.__month_combobox, \
        self.__gender_dob_widget, \
        self.__gender_dob_layout, \
        self.__school_info_layout, \
        self.__contact_info_layout, \
        self.__names_errors_widget, \
        self.__names_errors_layout, \
        self.__button_group_layout, \
        self.__gender_dob_errors_widget, \
        self.__gender_dob_errors_layout, \
        self.__gender_error_label, \
        self.__dob_error_label, \
        self.__personal_info_layout, \
        self.__last_name_error_label, \
        self.__city_state_zip_layout, \
        self.__city_state_zip_widget, \
        self.__school_info_group_box, \
        self.__contact_info_group_box, \
        self.__contact_info_group_box, \
        self.__first_name_error_label, \
        self.__personal_info_group_box, \
        self.__id_passport_error_label, \
        self.__country_tel_email_layout, \
        self.__country_tel_email_widget, \
        self.__course_department_branch_layout, \
        self.__course_department_branch_widget, \
        self.__credit__points, \
        self.__current_status = repeat(None, 67)

        self.load_ui()

    def init_tel_error_label(self) -> NoReturn:
        self.__tel_error_label = QLabel()

    def init_email_error_label(self) -> NoReturn:
        self.__email_error_label = QLabel()

    def init_tel_email_errors_widget(self) -> NoReturn:
        self.__tel_email_errors_widget = QWidget()

    def init_tel_email_errors_layout(self) -> NoReturn:
        self.__tel_email_errors_layout = QHBoxLayout()

    def init_male(self) -> NoReturn:
        self.__male = QRadioButton()

    def init_female(self) -> NoReturn:
        self.__female = QRadioButton()

    def init_dob_label(self) -> NoReturn:
        self.__dob_label = QLabel()

    def init_gender_error_label(self) -> NoReturn:
        self.__gender_error_label = QLabel()

    def init_dob_error_label(self) -> NoReturn:
        self.__dob_error_label = QLabel()

    def init_gender_dob_errors_widget(self) -> NoReturn:
        self.__gender_dob_errors_widget = QWidget()

    def init_gender_dob_errors_layout(self) -> NoReturn:
        self.__gender_dob_errors_layout = QHBoxLayout()

    def init_save_btn(self) -> NoReturn:
        self.__save_btn = QPushButton()

    def init_first_name_error_label(self) -> NoReturn:
        self.__first_name_error_label = QLabel()

    def init_id_passport_error_label(self) -> NoReturn:
        self.__id_passport_error_label = QLabel()

    def init_last_name_error_label(self) -> NoReturn:
        self.__last_name_error_label = QLabel()

    def init_names_errors_layout(self) -> NoReturn:
        self.__names_errors_layout = QHBoxLayout()

    def init_names_errors_widget(self) -> NoReturn:
        self.__names_errors_widget = QWidget()

    def init_day_combobox(self) -> NoReturn:
        self.__day_combobox = QComboBox()

    def init_month_combobox(self) -> NoReturn:
        self.__month_combobox = QComboBox()

    def init_year_combobox(self) -> NoReturn:
        self.__year_combobox = QComboBox()

    def init_gender_layout(self) -> NoReturn:
        self.__gender_layout = QHBoxLayout()

    def init_dob_layout(self) -> NoReturn:
        self.__dob_layout = QHBoxLayout()

    def init_dob_widget(self) -> NoReturn:
        self.__dob_widget = QWidget()

    def init_gender_widget(self) -> NoReturn:
        self.__gender_widget = QWidget()

    def init_id_passport(self):
        self.__id_passport = QLineEdit()

    def init_surname(self) -> NoReturn:
        self.__surname = QLineEdit()

    def init_first_name(self) -> NoReturn:
        self.__first_name = QLineEdit()

    def init_middle_name(self) -> NoReturn:
        self.__middle_name = QLineEdit()

    def init_names_widget(self) -> NoReturn:
        self.__names_widget = QWidget()

    def init_names_layout(self) -> NoReturn:
        self.__names_layout = QHBoxLayout()

    def init_gender_dob_widget(self) -> NoReturn:
        self.__gender_dob_widget = QWidget()

    def init_gender_dob_layout(self) -> NoReturn:
        self.__gender_dob_layout = QHBoxLayout()

    def init_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout = QVBoxLayout()
        self.__personal_info_layout.setAlignment(Qt.AlignTop)

    def init_personal_info_group_box(self) -> NoReturn:
        self.__personal_info_group_box = QGroupBox()

    def init_city(self) -> NoReturn:
        self.__city = QLineEdit()

    def init_state(self) -> NoReturn:
        self.__state = QLineEdit()

    def init_status(self) -> NoReturn:
        self.__status = QComboBox()

    def init_zip(self) -> NoReturn:
        self.__zip = QLineEdit()

    def init_course(self) -> NoReturn:
        self.__course = QComboBox()

    def init_branch(self) -> NoReturn:
        self.__branch = QComboBox()

    def init_department(self) -> NoReturn:
        self.__department = QComboBox()

    def init_country(self) -> NoReturn:
        self.__country = QComboBox()

    def init_button_group_layout(self) -> NoReturn:
        self.__button_group_layout = QHBoxLayout()

    def init_tel(self) -> NoReturn:
        self.__tel = QLineEdit()

    def init_email(self) -> NoReturn:
        self.__email = QLineEdit()

    def init_address1(self) -> NoReturn:
        self.__address1 = QLineEdit()

    def init_address2(self) -> NoReturn:
        self.__address2 = QLineEdit()

    def init_address_widget(self) -> NoReturn:
        self.__address_widget = QWidget()

    def init_address_layout(self) -> NoReturn:
        self.__address_layout = QHBoxLayout()

    def init_city_state_zip_widget(self) -> NoReturn:
        self.__city_state_zip_widget = QWidget()

    def init_city_state_zip_layout(self) -> NoReturn:
        self.__city_state_zip_layout = QHBoxLayout()

    def init_country_tel_email_widget(self) -> NoReturn:
        self.__country_tel_email_widget = QWidget()

    def init_country_tel_email_layout(self) -> NoReturn:
        self.__country_tel_email_layout = QHBoxLayout()

    def init_course_department_branch_widget(self) -> NoReturn:
        self.__course_department_branch_widget = QWidget()

    def init_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout = QHBoxLayout()

    def init_main_layout(self) -> NoReturn:
        self.__main_layout = QFormLayout()

    def init_school_info_layout(self) -> NoReturn:
        self.__school_info_layout = QVBoxLayout()

    def init_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout = QVBoxLayout()

    def init_school_info_group_box(self) -> NoReturn:
        self.__school_info_group_box = QGroupBox()

    def init_contact_info_group_box(self) -> NoReturn:
        self.__contact_info_group_box = QGroupBox()

    def init_status_widget(self) -> NoReturn:
        self.__status_widget = QWidget()

    def init_status_layout(self) -> NoReturn:
        self.__status_layout = QHBoxLayout()

    def setup_gender_error_label(self) -> NoReturn:
        self.__gender_error_label.setText("*Gender is required")
        self.__gender_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__gender_error_label.setVisible(True)

    def setup_male(self) -> NoReturn:
        self.__male.setText("Male")

    def setup_female(self) -> NoReturn:
        self.__female.setText("Female")

    def setup_tel_error_label(self) -> NoReturn:
        self.__tel_error_label.setText("*Mobile/Tel No is required")
        self.__tel_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__tel_error_label.setContentsMargins(0, 0, 0, 0)

    def setup_email_error_label(self) -> NoReturn:
        self.__email_error_label.setText("*Email is required")
        self.__email_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__email_error_label.setContentsMargins(0, 0, 0, 0)

    def setup_tel_email_errors_widget(self) -> NoReturn:
        self.__tel_email_errors_widget.setContentsMargins(0, 0, 0, 0)
        self.__tel_email_errors_widget.setLayout(self.__tel_email_errors_layout)

    def setup_tel_email_errors_layout(self) -> NoReturn:
        self.__tel_email_errors_layout.setContentsMargins(0, 0, 0, 0)

    def setup_dob_error_label(self) -> NoReturn:
        self.__dob_error_label.setText("*DOB is required")
        self.__dob_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__dob_error_label.setVisible(True)
        self.__dob_error_label.setContentsMargins(50, 0, 0, 0)

    def setup_address1_error_label(self) -> NoReturn:
        self.__address1_error_label.setText("*Address is required")
        self.__address1_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__address1_error_label.setVisible(True)
        self.__address1_error_label.setContentsMargins(0, 0, 0, 0)

    def setup_names_errors_widget(self) -> NoReturn:
        self.__names_errors_widget.setFixedHeight(40)
        self.__names_errors_widget.setContentsMargins(0, 0, 0, 0)
        self.__names_errors_widget.setLayout(self.__names_errors_layout)

    def setup_names_errors_layout(self) -> NoReturn:
        self.__names_errors_layout.setContentsMargins(0, 0, 0, 0)

    def setup_gender_dob_errors_widget(self) -> NoReturn:
        self.__gender_dob_errors_widget.setFixedHeight(40)
        self.__gender_dob_errors_widget.setContentsMargins(0, 0, 0, 10)
        self.__gender_dob_errors_widget.setLayout(self.__gender_dob_errors_layout)

    def setup_gender_dob_errors_layout(self) -> NoReturn:
        self.__gender_dob_errors_layout.setContentsMargins(0, 0, 0, 0)

    def setup_dob_label(self) -> NoReturn:
        self.__dob_label.setText("DOB: ")

    def setup_first_name_error_label(self) -> NoReturn:
        self.__first_name_error_label.setText("*First name is required")
        self.__first_name_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__first_name_error_label.setVisible(True)

    def setup_id_passport_error_label(self) -> NoReturn:
        self.__id_passport_error_label.setText("*Id/Passport No. is required")
        self.__id_passport_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__id_passport_error_label.setVisible(True)
        self.__id_passport_error_label.setContentsMargins(0, 10, 0, 0)

    def setup_last_name_error_label(self) -> NoReturn:
        self.__last_name_error_label.setText("*Surname is required")
        self.__last_name_error_label.setStyleSheet(
            """
            color: red;
            font-size: 10px;
            """
        )
        self.__last_name_error_label.setVisible(True)

    def setup_day_combobox(self) -> NoReturn:
        self.__day_combobox.setFixedSize(QSize(70, 25))
        self.__day_combobox.setStyleSheet(
            """
            border-radius: 1
            """
        )
        days = []
        for day in range(1, 32):
            if day < 10:
                days.append("0" + str(day))
            else:
                days.append(str(day))

        self.__day_combobox.addItems(days)

    def setup_month_combobox(self) -> NoReturn:
        self.__month_combobox.setFixedSize(QSize(70, 25))
        self.__month_combobox.setStyleSheet(
            """
            border-radius: 1
            """
        )
        months = []
        for month in range(1, 13):
            if month < 10:
                months.append("0" + str(month))
            else:
                months.append(str(month))
        self.__month_combobox.addItems(months)

    def setup_year_combobox(self) -> NoReturn:
        year = datetime.today().year
        start_year = year - 18
        end_year = start_year - 50

        self.__year_combobox.addItems([str(year) for year in range(end_year, start_year + 1)])
        self.__year_combobox.setCurrentText(str(start_year))
        self.__year_combobox.setStyleSheet(
            """
            border-radius: 1
            """
        )
        self.__year_combobox.setFixedSize(QSize(100, 25))
        self.__year_combobox.setContentsMargins(0, 0, 0, 0)

    def setup_gender_layout(self) -> NoReturn:
        self.__gender_layout.setContentsMargins(0, 0, 0, 0)
        self.__gender_layout.setAlignment(Qt.AlignLeft)
        self.__gender_layout.addWidget(QLabel("Gender: "))

    def setup_dob_layout(self) -> NoReturn:
        self.__dob_layout.setContentsMargins(0, 0, 0, 0)
        self.__dob_layout.setAlignment(Qt.AlignRight)

    def setup_first_name(self) -> NoReturn:
        self.__first_name.setFixedHeight(30)
        self.__first_name.setContentsMargins(0, 0, 0, 0)
        self.__first_name.setPlaceholderText("First Name...")

    def setup_middle_name(self) -> NoReturn:
        self.__middle_name.setFixedHeight(30)
        self.__middle_name.setPlaceholderText("Middle Name...")

    def setup_surname(self) -> NoReturn:
        self.__surname.setFixedHeight(30)
        self.__surname.setPlaceholderText("Surname...")

    def setup_id_passport(self) -> NoReturn:
        self.__id_passport.setPlaceholderText("ID./Passport No...")
        self.__id_passport.setFixedSize(QSize(182, 30))
        self.__id_passport.setContentsMargins(0, 0, 0, 0)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_lines(painter)
        painter.end()

    def draw_lines(self, painter):
        pen = QPen(Qt.black, 2, Qt.SolidLine)

        painter.setPen(pen)

        painter.drawLine(710, 32, 740, 32)
        painter.drawLine(380, 680, 385, 680)

    def setup_main_layout(self) -> NoReturn:
        self.setObjectName("add_student_dialog")
        self.setWindowTitle("Add Student")
        self.setFixedSize(QSize(770, 700))
        self.setLayout(self.__main_layout)

    def setup_personal_info_group_box(self) -> NoReturn:
        self.__personal_info_group_box.setTitle("Personal Info")
        self.__personal_info_group_box.setFixedSize(QSize(730, 220))
        self.__personal_info_group_box.setLayout(self.__personal_info_layout)

    def setup_names_layout(self) -> NoReturn:
        self.__names_layout.setContentsMargins(0, 0, 0, 0)

    def setup_gender_widget(self) -> NoReturn:
        self.__gender_widget.setContentsMargins(0, 0, 0, 0)
        self.__gender_widget.setLayout(self.__gender_layout)

    def setup_save_btn(self) -> NoReturn:
        self.__save_btn.setText("Save")
        self.__save_btn.setFixedSize(100, 40)
        self.__save_btn.setStyleSheet(
            """
            background-color: teal;
            color: white
            """
        )
        self.__save_btn.clicked.connect(self.on_submit)

    def setup_dob_widget(self) -> NoReturn:
        self.__dob_widget.setContentsMargins(0, 0, 0, 0)
        self.__dob_widget.setLayout(self.__dob_layout)

    def setup_names_widget(self) -> NoReturn:
        self.__names_widget.setFixedHeight(40)
        self.__names_widget.setContentsMargins(0, 0, 0, 0)
        self.__names_widget.setLayout(self.__names_layout)

    def setup_gender_dob_layout(self) -> NoReturn:
        self.__gender_dob_layout.setContentsMargins(0, 0, 0, 0)

    def setup_gender_dob_widget(self) -> NoReturn:
        self.__gender_dob_widget.setFixedHeight(40)
        self.__gender_dob_widget.setContentsMargins(0, 0, 0, 0)
        self.__gender_dob_widget.setLayout(self.__gender_dob_layout)

    def setup_button_group_layout(self) -> NoReturn:
        self.__button_group_layout.addSpacing(520)
        self.__button_group_layout.setContentsMargins(0, 20, 0, 0)
        cancel_btn = QPushButton()
        cancel_btn.setText("Cancel")
        cancel_btn.setFixedSize(100, 40)
        cancel_btn.setStyleSheet(
            """
            background-color: tomato;
            color: white
            """
        )
        cancel_btn.clicked.connect(self.close)

        self.__button_group_layout.addWidget(cancel_btn)

    def setup_address1(self) -> NoReturn:
        self.__address1.setContentsMargins(0, 0, 0, 0)
        self.__address1.setPlaceholderText("Address Line 1...")
        self.__address1.setFixedHeight(30)

    def setup_address2(self) -> NoReturn:
        self.__address2.setContentsMargins(0, 0, 0, 0)
        self.__address2.setPlaceholderText("Address Line 2...")
        self.__address2.setFixedHeight(30)

    def setup_city(self) -> NoReturn:
        self.__city.setFixedHeight(30)
        self.__city.setContentsMargins(0, 0, 0, 0)
        self.__city.setPlaceholderText("City...")

    def setup_state(self) -> NoReturn:
        self.__state.setFixedHeight(30)
        self.__state.setContentsMargins(0, 0, 0, 0)
        self.__state.setPlaceholderText("State...")

    def setup_zip(self) -> NoReturn:
        self.__zip.setFixedHeight(30)
        self.__zip.setContentsMargins(0, 0, 0, 0)
        self.__zip.setPlaceholderText("Zip...")

    def setup_country(self) -> NoReturn:
        countries = ["Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Anguilla", "Antigua & Barbuda",
                     "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain",
                     "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia",
                     "Bosnia & Herzegovina", "Botswana", "Brazil", "British Virgin Islands", "Brunei", "Bulgaria",
                     "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Cape Verde", "Cayman Islands", "Chad", "Chile",
                     "China", "Colombia", "Congo", "Cook Islands", "Costa Rica", "Cote D Ivoire", "Croatia",
                     "Cruise Ship", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
                     "Dominican Republic", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Estonia",
                     "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Polynesia",
                     "French West Indies", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece",
                     "Greenland", "Grenada", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea Bissau", "Guyana",
                     "Haiti", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
                     "Ireland", "Isle of Man", "Israel", "Italy", "Jamaica", "Japan", "Jersey", "Jordan", "Kazakhstan",
                     "Kenya", "Kuwait", "Kyrgyz Republic", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
                     "Liechtenstein", "Lithuania", "Luxembourg", "Macau", "Macedonia", "Madagascar", "Malawi",
                     "Malaysia", "Maldives", "Mali", "Malta", "Mauritania", "Mauritius", "Mexico", "Moldova", "Monaco",
                     "Mongolia", "Montenegro", "Montserrat", "Morocco", "Mozambique", "Namibia", "Nepal", "Netherlands",
                     "Netherlands Antilles", "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Norway",
                     "Oman", "Pakistan", "Palestine", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
                     "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion", "Romania", "Russia", "Rwanda",
                     "Saint Pierre & Miquelon", "Samoa", "San Marino", "Satellite", "Saudi Arabia", "Senegal", "Serbia",
                     "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "South Africa", "South Korea",
                     "Spain", "Sri Lanka", "St Kitts & Nevis", "St Lucia", "St Vincent", "St. Lucia", "Sudan",
                     "Suriname", "Swaziland", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
                     "Thailand", "Timor L'Este", "Togo", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey",
                     "Turkmenistan", "Turks & Caicos", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
                     "Uruguay", "Uzbekistan", "Venezuela", "Vietnam", "Virgin Islands (US)", "Yemen", "Zambia",
                     "Zimbabwe"]

        self.__country.setFixedHeight(25)
        self.__country.setContentsMargins(0, 0, 0, 0)
        self.__country.addItems(countries)
        self.__country.setCurrentText("Kenya")
        self.__country.setStyleSheet(
            """
            border-radius: 1
            """
        )

    def setup_tel(self) -> NoReturn:
        self.__tel.setFixedHeight(30)
        self.__tel.setContentsMargins(0, 0, 0, 0)
        self.__tel.setPlaceholderText("Mobile/Tel No(+254)...")

    def setup_email(self) -> NoReturn:
        self.__email.setFixedHeight(30)
        self.__email.setContentsMargins(0, 0, 0, 0)
        self.__email.setPlaceholderText("Email address...")

    def setup_course(self) -> NoReturn:
        self.__course.setFixedSize(QSize(150, 25))
        self.__course.setStyleSheet(
            """
            border-radius: 1
            """
        )
        courses = [course["course_title"] for course in
                   self.table_docs(BaseConfig.db, BaseConfig.courses_table)]
        self.__course.addItems(courses)

    def setup_department(self) -> NoReturn:
        self.__department.setFixedSize(QSize(150, 25))
        self.__department.setStyleSheet(
            """
            border-radius: 1
            """
        )
        departments = [department["title"] for department in
                       self.table_docs(BaseConfig.db, BaseConfig.departments_table)]
        self.__department.addItems(departments)

    def setup_branch(self) -> NoReturn:
        self.__branch.setFixedSize(QSize(150, 25))
        self.__branch.setStyleSheet(
            """
            border-radius: 1
            """
        )
        branches = [branch["title"] for branch in self.table_docs(BaseConfig.db, BaseConfig.branches_table)]

        self.__branch.addItems(branches)

    def setup_status(self) -> NoReturn:
        self.__status.setFixedSize(QSize(150, 25))
        self.__status.setContentsMargins(0, 0, 0, 0)
        self.__status.setStyleSheet(
            """
            border-radius: 1
            """
        )
        self.__status.addItems([status for status in ["active", "deactivated", "pending"]])
        self.__status.setCurrentText("pending")

    def setup_address_layout(self) -> NoReturn:
        self.__address_layout.setContentsMargins(0, 0, 0, 0)

    def setup_address_widget(self) -> NoReturn:
        self.__address_widget.setContentsMargins(0, 0, 0, 0)
        self.__address_widget.setLayout(self.__address_layout)

    def setup_status_layout(self) -> NoReturn:
        self.__status_layout.setContentsMargins(0, 0, 0, 0)
        self.__status_layout.setAlignment(Qt.AlignLeft)

    def setup_status_widget(self) -> NoReturn:
        self.__status_widget.setContentsMargins(0, 0, 0, 0)
        self.__status_widget.setFixedWidth(300)
        self.__status_widget.setLayout(self.__status_layout)

    def setup_city_state_zip_widget(self) -> NoReturn:
        self.__city_state_zip_widget.setContentsMargins(0, 0, 0, 0)
        self.__city_state_zip_widget.setLayout(self.__city_state_zip_layout)

    def setup_city_state_zip_layout(self) -> NoReturn:
        self.__city_state_zip_layout.setContentsMargins(0, 0, 0, 0)

    def setup_country_tel_email_widget(self) -> NoReturn:
        self.__country_tel_email_widget.setContentsMargins(0, 0, 0, 0)
        self.__country_tel_email_widget.setLayout(self.__country_tel_email_layout)

    def setup_country_tel_email_layout(self) -> NoReturn:
        self.__country_tel_email_layout.setContentsMargins(0, 0, 0, 0)
        self.__country_tel_email_layout.setAlignment(Qt.AlignLeft)

    def setup_course_department_branch_widget(self) -> NoReturn:
        self.__course_department_branch_widget.setContentsMargins(0, 0, 0, 0)
        self.__course_department_branch_widget.setLayout(self.__course_department_branch_layout)

    def setup_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.setContentsMargins(0, 0, 0, 0)

    def setup_school_info_groupbox(self) -> NoReturn:
        self.__school_info_group_box.setContentsMargins(0, 0, 0, 0)
        self.__school_info_group_box.setTitle("School Info")
        self.__school_info_group_box.setFixedSize(QSize(730, 120))
        self.__school_info_group_box.setLayout(self.__school_info_layout)

    def setup_contact_info_groupbox(self) -> NoReturn:
        self.__contact_info_group_box.setContentsMargins(0, 0, 0, 0)
        self.__contact_info_group_box.setTitle("Contact Info")
        self.__contact_info_group_box.setFixedSize(QSize(730, 180))
        self.__contact_info_group_box.setLayout(self.__contact_info_layout)

    def add_save_btn_to_button_group_layout(self) -> NoReturn:
        self.__button_group_layout.addWidget(self.__save_btn)

    def add_tel_email_errors_widget_to_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout.addWidget(self.__tel_email_errors_widget)

    def add_tel_error_label_to_tel_email_errors_layout(self) -> NoReturn:
        self.__tel_email_errors_layout.addSpacing(170)
        self.__tel_email_errors_layout.addWidget(self.__tel_error_label)

    def add_email_error_label_to_tel_email_errors_layout(self) -> NoReturn:
        self.__tel_email_errors_layout.addWidget(self.__email_error_label)

    def add_header_to_main_layout(self) -> NoReturn:
        header = QLabel("Students Onboarding")

        header_layout = QHBoxLayout()
        header_layout.addSpacing(580)
        header_layout.addWidget(header)

        self.__main_layout.addRow("", header_layout)

    def add_personal_info_group_box_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__personal_info_group_box)

    def add_male_to_gender_layout(self) -> NoReturn:
        self.__gender_layout.addWidget(self.__male)

    def add_female_to_gender_layout(self) -> NoReturn:
        self.__gender_layout.addWidget(self.__female)

    def add_names_widget_to_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__names_widget)

    def add_names_errors_widget_to_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__names_errors_widget)

    def add_first_name_error_label_to_names_errors_layout(self) -> NoReturn:
        self.__names_errors_layout.addWidget(self.__first_name_error_label)
        self.__names_errors_layout.addStretch(1)

    def add_middle_name_error_label_to_names_errors_layout(self) -> NoReturn:
        self.__names_errors_layout.addWidget(self.__middle_name_error_label)

    def add_last_name_error_label_to_names_errors_layout(self) -> NoReturn:
        self.__names_errors_layout.addWidget(self.__last_name_error_label)

    def add_id_passport_to_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__id_passport)

    def add_id_passport_error_label_to_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__id_passport_error_label)

    def add_gender_dob_widget_to_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__gender_dob_widget)

    def add_first_name_to_names_widget(self) -> NoReturn:
        self.__names_layout.addWidget(self.__first_name)

    def add_middle_to_names_widget(self) -> NoReturn:
        self.__names_layout.addWidget(self.__middle_name)

    def add_surname_to_names_widget(self) -> NoReturn:
        self.__names_layout.addWidget(self.__surname)

    def add_gender_widget_to_gender_dob_layout(self) -> NoReturn:
        self.__gender_dob_layout.addWidget(self.__gender_widget)

    def add_dob_widget_to_gender_dob_layout(self) -> NoReturn:
        self.__gender_dob_layout.addWidget(self.__dob_widget)

    def add_dob_label_to_dob_layout(self) -> NoReturn:
        self.__dob_layout.addWidget(self.__dob_label)

    def add_day_combobox_to_dob_layout(self) -> NoReturn:
        self.__dob_layout.addWidget(self.__day_combobox)

    def add_month_combobox_to_dob_layout(self) -> NoReturn:
        self.__dob_layout.addWidget(self.__month_combobox)

    def add_year_combobox_to_dob_layout(self) -> NoReturn:
        self.__dob_layout.addWidget(self.__year_combobox)

    def add_gender_dob_errors_widget_to_personal_info_layout(self) -> NoReturn:
        self.__personal_info_layout.addWidget(self.__gender_dob_errors_widget)

    def add_gender_error_label_to_gender_dob_errors_layout(self) -> NoReturn:
        self.__gender_dob_errors_layout.addWidget(self.__gender_error_label)

    def add_dob_error_label_to_gender_dob_errors_layout(self) -> NoReturn:
        self.__gender_dob_errors_layout.addWidget(self.__dob_error_label)

    def add_contact_info_group_box_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__contact_info_group_box)

    def add_school_info_group_box_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__school_info_group_box)

    def add_button_group_to_layout(self) -> NoReturn:
        self.__main_layout.addRow("", self.__button_group_layout)

    def add_address_widget_to_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout.addWidget(self.__address_widget)

    def add_city_state_zip_widget_to_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout.addWidget(self.__city_state_zip_widget)

    def add_course_department_branch_widget_to_school_info_layout(self) -> NoReturn:
        self.__school_info_layout.addWidget(self.__course_department_branch_widget)

    def add_status_widget_to_school_info_layout(self) -> NoReturn:
        self.__school_info_layout.addWidget(self.__status_widget)

    def add_status_label_to_status_layout(self) -> NoReturn:
        self.__status_layout.addWidget(QLabel("Status:  "))

    def add_status_to_status_layout(self) -> NoReturn:
        self.__status_layout.addWidget(self.__status)

    def add_country_tel_email_widget_to_contact_info_layout(self) -> NoReturn:
        self.__contact_info_layout.addWidget(self.__country_tel_email_widget)

    def add_course_label_to_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.addWidget(QLabel("Course: "))

    def add_course_to_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.addWidget(self.__course)

    def add_department_label_to_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.addWidget(QLabel("Department: "))

    def add_department_to_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.addWidget(self.__department)

    def add_branch_label_to_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.addWidget(QLabel("Branch: "))

    def add_branch_to_course_department_branch_layout(self) -> NoReturn:
        self.__course_department_branch_layout.addWidget(self.__branch)

    def add_city_to_city_state_zip_layout(self) -> NoReturn:
        self.__city_state_zip_layout.addWidget(self.__city)

    def add_state_to_city_state_zip_layout(self) -> NoReturn:
        self.__city_state_zip_layout.addWidget(self.__state)

    def add_zip_to_city_state_zip_layout(self) -> NoReturn:
        self.__city_state_zip_layout.addWidget(self.__zip)

    def add_country_to_country_tel_email_layout(self) -> NoReturn:
        self.__country_tel_email_layout.addWidget(self.__country)

    def add_tel_to_country_tel_email_layout(self) -> NoReturn:
        self.__country_tel_email_layout.addWidget(self.__tel)

    def add_email_to_country_tel_email_layout(self) -> NoReturn:
        self.__country_tel_email_layout.addWidget(self.__email)

    def add_address1_to_address_layout(self) -> NoReturn:
        self.__address_layout.addWidget(self.__address1)

    def add_address2_to_address_layout(self) -> NoReturn:
        self.__address_layout.addWidget(self.__address2)

    def set_messages(self, *args) -> NoReturn:
        self.__student_id = args[0]
        self.__first_name.setText(args[1])
        self.__middle_name.setText(args[2])
        self.__surname.setText(args[3])
        if args[4] == "Male":
            self.__male.toggle()
        elif args[4] == "Female":
            self.__female.toggle()
        self.__day_combobox.setCurrentText(args[5][:2])
        self.__month_combobox.setCurrentText(args[5][3:5])
        self.__year_combobox.setCurrentText(args[5][6:])
        self.__id_passport.setText(args[6])
        self.__address1.setText(args[7])
        self.__address2.setText(args[8])
        self.__city.setText(args[9])
        self.__state.setText(args[10])
        self.__zip.setText(args[11])
        self.__country.setCurrentText(args[12])
        self.__tel.setText(args[13])
        self.__email.setText(args[14])
        self.__course.setCurrentText(args[15])
        self.__department.setCurrentText(args[16])
        self.__branch.setCurrentText(args[17])
        self.__status.setCurrentText(args[18])
        self.__current_status = args[18]

    def save_file(self, filepath):
        fh = open(filepath, 'rb')
        contents = fh.read()
        fh.close()
        doc_to_update = {"id": self.__student_id, "filename": filepath, "file": r.binary(contents)}

        self.update_doc(BaseConfig.db, BaseConfig.files_table, doc_to_update, self.__student_id)

    def on_submit(self) -> NoReturn:
        gender = None
        first_name = self.__first_name.text()
        middle_name = self.__middle_name.text()
        surname = self.__surname.text()
        male = self.__male.isChecked()
        female = self.__female.isChecked()
        dob = self.__day_combobox.currentText() + "-" + self.__month_combobox.currentText() + "-" + self.__year_combobox.currentText()
        id_passport = self.__id_passport.text()
        address1 = self.__address1.text()
        address2 = self.__address2.text()
        country = self.__country.currentText()
        city = self.__city.text()
        state = self.__state.text()
        zip = self.__zip.text()
        email = self.__email.text()
        tel = self.__tel.text()
        course = self.__course.currentText()
        department = self.__department.currentText()
        branch = self.__branch.currentText()
        status = self.__status.currentText()

        course_count = self.__course.count()
        branch_count = self.__branch.count()
        department_count = self.__department.count()

        if course_count == 0 or department_count == 0 or branch_count == 0:
            if course_count == 0:
                QMessageBox.critical(self, "Critical", "Go to courses page to add courses before proceeding...")
                self.close()
            elif department_count == 0:
                QMessageBox.critical(self, "Critical", "Go to departments page to add departments before proceeding...")
                self.close()
            elif branch_count == 0:
                QMessageBox.critical(self, "Critical", "Go to branches page to add branches before proceeding...")
                self.close()
        else:
            if not (male or female) or not (first_name and surname and id_passport and tel and email):
                QMessageBox.critical(self, "Critical", "Missing 1 or more required arguments")
            else:
                if male:
                    gender = "Male"
                elif female:
                    gender = "Female"

                doc_to_be_updated = {
                    "first_name": first_name,
                    "middle_name": middle_name,
                    "surname": surname,
                    "gender": gender,
                    "dob": dob,
                    "id_passport": id_passport,
                    "city": city,
                    "state": state,
                    "zip": zip,
                    "address1": address1,
                    "address2": address2,
                    "country": country,
                    "tel": tel,
                    "email": email,
                    "course": course,
                    "department": department,
                    "branch": branch,
                    "status": status,
                    "expiry_date": end_dated
                }
                print(self.__current_status)
                print(status)

                qrcode_data = {"student_id": self.__student_id, "status": doc_to_be_updated["status"],
                               "expiry_date": doc_to_be_updated["expiry_date"], "credit__points": self.__credit__points}
                to_added = "qrcode_images/" + str(self.__student_id) + ".png"
                filename = str(Path(__file__).parents[3].joinpath(to_added))
                encode_data_to_file(qrcode_data, filename)
                self.save_file(filename)

                doc_update_result = self.update_doc(BaseConfig.db, BaseConfig.students_table, doc_to_be_updated,
                                                    self.__student_id)

                if doc_update_result["result"]:
                    if self.__current_status != status:
                        first_name = doc_to_be_updated['first_name'].capitalize()
                        surname = doc_to_be_updated['surname'].capitalize()
                        full_name = f"{first_name} {surname}"

                        q = Queue(maxsize=1)
                        m = Messenger(self.__student_id, full_name, "active")
                        Thread(target=self.send_message, args=(str(m), doc_to_be_updated["tel"], q,)).start()

                        message_result = q.get()
                        status_update_message = f"Student status updated successfully. {message_result['msg']}"
                        QMessageBox.information(self, "Success", status_update_message)
                        self.close()
                    else:
                        QMessageBox.information(self, "Success", "Student updated successfully")
                        self.close()
                else:
                    QMessageBox.critical(self, "Critical", doc_update_result["msg"])

    def load_ui(self):
        self.init_zip()
        self.init_tel()
        self.init_city()
        self.init_email()
        self.init_state()
        self.init_branch()
        self.init_course()
        self.init_status()
        self.init_country()
        self.init_surname()
        self.init_address1()
        self.init_address2()
        self.init_dob_label()
        self.init_department()
        self.init_dob_layout()
        self.init_dob_widget()
        self.init_first_name()
        self.init_main_layout()
        self.init_middle_name()
        self.init_id_passport()
        self.init_save_btn()
        self.init_male()
        self.init_female()
        self.init_day_combobox()
        self.init_names_layout()
        self.init_names_widget()
        self.init_status_widget()
        self.init_status_layout()
        self.init_year_combobox()
        self.init_gender_widget()
        self.init_gender_layout()
        self.init_address_widget()
        self.init_address_layout()
        self.init_month_combobox()
        self.init_gender_dob_errors_widget()
        self.init_gender_dob_errors_layout()
        self.init_gender_error_label()
        self.init_dob_error_label()
        self.init_names_errors_widget()
        self.init_names_errors_layout()
        self.init_school_info_layout()
        self.init_contact_info_layout()
        self.init_button_group_layout()
        self.init_gender_dob_widget()
        self.init_gender_dob_layout()
        self.init_personal_info_layout()
        self.init_tel_email_errors_widget()
        self.init_tel_email_errors_layout()
        self.init_tel_error_label()
        self.init_email_error_label()
        self.init_id_passport_error_label()
        self.init_last_name_error_label()
        self.init_city_state_zip_widget()
        self.init_city_state_zip_layout()
        self.init_school_info_group_box()
        self.init_first_name_error_label()
        self.init_contact_info_group_box()
        self.init_personal_info_group_box()
        self.init_country_tel_email_widget()
        self.init_country_tel_email_layout()
        self.init_course_department_branch_layout()
        self.init_course_department_branch_widget()

        self.setup_personal_info_group_box()
        self.setup_names_widget()
        self.setup_names_layout()
        self.setup_first_name()
        self.setup_middle_name()
        self.setup_surname()
        self.setup_names_errors_widget()
        self.setup_names_errors_layout()
        self.setup_first_name_error_label()
        self.setup_last_name_error_label()
        self.setup_gender_dob_widget()
        self.setup_gender_dob_layout()
        self.setup_gender_widget()
        self.setup_gender_layout()
        self.setup_male()
        self.setup_female()
        self.setup_dob_layout()
        self.setup_dob_widget()
        self.setup_dob_label()
        self.setup_day_combobox()
        self.setup_month_combobox()
        self.setup_year_combobox()
        self.setup_gender_dob_errors_widget()
        self.setup_gender_dob_errors_layout()
        self.setup_gender_error_label()
        self.setup_dob_error_label()
        self.setup_id_passport()
        self.setup_id_passport_error_label()
        self.setup_contact_info_groupbox()
        self.setup_address_widget()
        self.setup_address_layout()
        self.setup_address1()
        self.setup_address2()
        self.setup_city_state_zip_widget()
        self.setup_city_state_zip_layout()
        self.setup_city()
        self.setup_state()
        self.setup_zip()
        self.setup_country_tel_email_widget()
        self.setup_country_tel_email_layout()
        self.setup_country()
        self.setup_tel()
        self.setup_email()
        self.setup_tel_email_errors_widget()
        self.setup_tel_email_errors_layout()
        self.setup_tel_error_label()
        self.setup_email_error_label()
        self.setup_school_info_groupbox()
        self.setup_course_department_branch_widget()
        self.setup_course_department_branch_layout()
        self.setup_course()
        self.setup_department()
        self.setup_branch()
        self.setup_status_widget()
        self.setup_status_layout()
        self.setup_status()
        self.setup_button_group_layout()
        self.setup_save_btn()

        self.add_header_to_main_layout()

        self.add_personal_info_group_box_to_layout()
        self.add_names_widget_to_personal_info_layout()
        self.add_first_name_to_names_widget()
        self.add_middle_to_names_widget()
        self.add_surname_to_names_widget()
        self.add_names_errors_widget_to_personal_info_layout()
        self.add_first_name_error_label_to_names_errors_layout()
        self.add_last_name_error_label_to_names_errors_layout()
        self.add_gender_dob_widget_to_personal_info_layout()
        self.add_gender_widget_to_gender_dob_layout()
        self.add_male_to_gender_layout()
        self.add_female_to_gender_layout()
        self.add_dob_widget_to_gender_dob_layout()
        self.add_dob_label_to_dob_layout()
        self.add_day_combobox_to_dob_layout()
        self.add_month_combobox_to_dob_layout()
        self.add_year_combobox_to_dob_layout()
        self.add_gender_dob_errors_widget_to_personal_info_layout()
        self.add_gender_error_label_to_gender_dob_errors_layout()
        self.add_dob_error_label_to_gender_dob_errors_layout()
        self.add_id_passport_to_personal_info_layout()
        self.add_id_passport_error_label_to_personal_info_layout()

        self.add_contact_info_group_box_to_layout()
        self.add_address_widget_to_contact_info_layout()
        self.add_address1_to_address_layout()
        self.add_address2_to_address_layout()
        self.add_city_state_zip_widget_to_contact_info_layout()
        self.add_city_to_city_state_zip_layout()
        self.add_state_to_city_state_zip_layout()
        self.add_zip_to_city_state_zip_layout()
        self.add_country_tel_email_widget_to_contact_info_layout()
        self.add_country_to_country_tel_email_layout()
        self.add_tel_to_country_tel_email_layout()
        self.add_email_to_country_tel_email_layout()
        self.add_tel_email_errors_widget_to_contact_info_layout()
        self.add_tel_error_label_to_tel_email_errors_layout()
        self.add_email_error_label_to_tel_email_errors_layout()

        self.add_school_info_group_box_to_layout()
        self.add_course_department_branch_widget_to_school_info_layout()
        self.add_course_label_to_course_department_branch_layout()
        self.add_course_to_course_department_branch_layout()
        self.add_department_label_to_course_department_branch_layout()
        self.add_department_to_course_department_branch_layout()
        self.add_branch_label_to_course_department_branch_layout()
        self.add_branch_to_course_department_branch_layout()
        self.add_status_widget_to_school_info_layout()
        self.add_status_label_to_status_layout()
        self.add_status_to_status_layout()

        self.add_button_group_to_layout()
        self.add_save_btn_to_button_group_layout()

        self.setup_main_layout()
