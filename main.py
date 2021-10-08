from controller import Controller

import sys

from PyQt5 import QtCore, QtWidgets, uic


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_mywindow()
    sys.exit(app.exec_())