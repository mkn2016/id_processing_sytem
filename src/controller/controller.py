from typing import NoReturn

from src.views.window.window import MainWindow
from src.views.login.login import Login


class Controller:

    def __init__(self, settings):
        self.settings = settings
        self.login = Login(self.settings)
        self.window = MainWindow(self.settings)

    def show_login(self) -> NoReturn:
        self.window.close()
        self.login.show()
        self.login.switch_window.connect(self.show_main)

    def show_main(self) -> NoReturn:
        self.login.close()
        self.login.submitted.connect(self.window.on_submitted)
        self.window.showFullScreen()
        self.window.switch_window.connect(self.show_login)
