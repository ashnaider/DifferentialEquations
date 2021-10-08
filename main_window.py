from PyQt5 import QtCore, QtWidgets, uic

main_window_ui = 'UI\main_window.ui'
form, base = uic.loadUiType(uifile=main_window_ui)

class MainWindow(base, form):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(base, self).__init__()
        self.setupUi(self)

        self.toDiffEq_btn.clicked.connect(self.switch)

    def switch(self):
        self.switch_window.emit("from main window")