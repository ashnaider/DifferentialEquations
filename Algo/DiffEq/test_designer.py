import math
import sys
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic

import matplotlib
matplotlib.use('QT5Agg')

import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# uifile_1 = 'UI\diff_eq_window_without_layouts.ui'
uifile_1 = 'UI\diff_eq_widget_without_layouts.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

uifile_2 = 'UI\second_test_widget.ui'
form_2, base_2 = uic.loadUiType(uifile_2)

class MyWindow(base_1, form_1):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(base_1, self).__init__()
        self.setupUi(self)
        # uic.loadUi('gui_elements_set.ui', self) 
        # test data
        data = np.array([0.7,0.7,0.7,0.8,0.9,0.9,1.5,1.5,1.5,1.5])        
        fig, ax1 = plt.subplots()
        bins = np.arange(0.6, 1.62, 0.02)
        n1, bins1, patches1 = ax1.hist(data, bins, alpha=0.6, density=False, cumulative=False)
        fig, ax = plt.subplots()
        x = np.arange(0, 5, 0.1)
        y = [math.sin(i) for i in x]
        ax.plot(x, y, label="sinus")
        # plot
        self.plotWidget = FigureCanvas(fig)
        self.toolbar = NavigationToolbar(self.plotWidget, self)
        lay = QtWidgets.QVBoxLayout(self.plot_widget)  
        # lay.setContentsMargins(0, 0, 0, 0)      
        lay.addWidget(self.toolbar)
        lay.addWidget(self.plotWidget)

        back = QtWidgets.QPushButton("back")
        back.clicked.connect(self.switch)
        lay.addWidget(back)
        # add toolbar
        # self.addToolBar(QtCore.Qt.TopToolBarArea, NavigationToolbar(self.plotWidget, self))

    def switch(self):
        self.switch_window.emit("from first")


class SecondWindow(base_2, form_2):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(base_2, self).__init__()
        self.setupUi(self)

        # back = QtWidgets.QPushButton(self.back_btn)  
        self.back_btn.clicked.connect(self.switch) 
        

    def switch(self):
        self.switch_window.emit("from second")



class Controller():
    def __init__(self):
        pass
        self.login = MyWindow()
        self.two = SecondWindow()
        self.login_opened = False
        self.two_opened = False

    def show_mywindow(self):
        self.login = MyWindow()
        self.login.switch_window.connect(self.show_secondwindow)

        if self.two_opened:
            self.two.close()
            self.two_opened = False

        self.login.show()
        self.login_opened = True


    def show_secondwindow(self):
        self.two = SecondWindow()
        self.two.switch_window.connect(self.show_mywindow)
        if self.login_opened:
            self.login.close()
            self.login_opened = False

        self.two.show()
        self.two_opened = True

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_mywindow()
    sys.exit(app.exec_())