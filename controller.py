from diff_eq_window import DiffEqWindow
from main_window import MainWindow

from PyQt5 import QtCore, QtWidgets, uic


class Controller():
    def __init__(self):
        pass
        self.main_window = MainWindow()
        self.diff_eq_window = DiffEqWindow()
        self.login_opened = False
        self.two_opened = False

    def show_mywindow(self):
        self.login = MainWindow()
        self.login.switch_window.connect(self.show_secondwindow)

        if self.two_opened:
            self.diff_eq_window.close()
            self.two_opened = False

        self.login.show()
        self.login_opened = True


    def show_secondwindow(self):
        self.diff_eq_window = DiffEqWindow()
        self.diff_eq_window.switch_window.connect(self.show_mywindow)
        if self.login_opened:
            self.login.close()
            self.login_opened = False

        self.diff_eq_window.show()
        self.two_opened = True