import math
import sys
from PyQt5.QtGui import QDoubleValidator
import numpy as np

from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog, QPushButton, QToolBar, QAction

import matplotlib
from pandas.core.accessor import PandasDelegate
matplotlib.use('QT5Agg')
import matplotlib.pylab as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas 
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from Algo.DiffEq.Euler_Cauchy_method import *
from Algo.DiffEq.Euler_diff_eq_method import *
from Algo.DiffEq.Runge_Kutta import *
from Algo.DiffEq.midpoint_method import *

from Utils.dataframe_model import DataFrameModel
from Utils.files import *
from Utils.string_parser import *

integral_window = 'UI\diff_eq_main_window.ui'
form, base = uic.loadUiType(uifile=integral_window)

class DiffEqWindow(base, form):
    switch_window = QtCore.pyqtSignal(str)

    def __init__(self):
        super(base, self).__init__()
        self.setupUi(self)

        self.connect_canvas()

        self.connect_buttons()

        self.activate_plot_buttons(False)

        self.set_line_edits()

        self.connect_toolbar_actions()

        self.settings_norm = False
        self.setting_for_solution_norm = False
        self.sol = None

        self.got_tables = False
        self.curr_all_h1 = None
        self.curr_res_h1 = None
        self.curr_all_h2 = None
        self.curr_res_h2 = None
        

    def get_diff_eq_line_edits(self):
        return [ self.x0_le, self.y0_le, 
                 self.diff_eq_a_le, self.diff_eq_b_le,
                 self.diff_eq_h1_le, self.diff_eq_h2_le
                ]

    def get_solution_line_edits(self):
        return [
            self.solution_a_le,
            self.solution_b_le,
            self.solution_h_le
        ]

    def connect_canvas(self):
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        lay = QtWidgets.QVBoxLayout(self.plot_widget)  
        lay.addWidget(self.toolbar)
        lay.addWidget(self.canvas)

    def set_line_edits(self):
        validator = QDoubleValidator(1000, -1000, 4)

        self.x0_le.setValidator(validator)
        self.y0_le.setValidator(validator)

        self.diff_eq_a_le.setValidator(validator)
        self.diff_eq_b_le.setValidator(validator)

        self.diff_eq_h1_le.setValidator(validator)
        self.diff_eq_h2_le.setValidator(validator)

        self.solution_a_le.setValidator(validator)
        self.solution_b_le.setValidator(validator)
        self.solution_h_le.setValidator(validator)

    def connect_toolbar_actions(self):
        self.save_all_h1_action.triggered.connect(self.save_prepare)
        self.save_all_h2_action.triggered.connect(self.save_prepare)
        self.save_res_h1_action.triggered.connect(self.save_prepare)
        self.save_res_h2_action.triggered.connect(self.save_prepare)

        self.open_file_action.triggered.connect(self.upload_data_from_file)
        

    def connect_buttons(self):
        self.Runge_Kutta_method_btn.clicked.connect(self.plot_Runge_Kutta)
        self.Eulers_method_btn.clicked.connect(self.plot_Euler_method)
        self.Eulers_Cauchy_method_btn.clicked.connect(self.plot_Euler_Cauchy_method)
        self.midpoint_method_btn.clicked.connect(self.plot_midpoint_method)
        self.actual_solution_btn.clicked.connect(self.plot_actual_solution)

        self.back_btn.clicked.connect(self.switch)

        self.check_settings_btn.clicked.connect(self.check_settings)

        self.clear_canvas_btn.clicked.connect(self.clear_canvas)
        self.clear_tables_btn.clicked.connect(self.clear_tables)
        self.clear_all_btn.clicked.connect(self.clear_all)

        self.save_all_h1_btn.clicked.connect(self.save_prepare)
        self.save_all_h2_btn.clicked.connect(self.save_prepare)
        self.save_res_h1_btn.clicked.connect(self.save_prepare)
        self.save_res_h2_btn.clicked.connect(self.save_prepare)

        self.upload_data_from_file_btn.clicked.connect(self.upload_data_from_file)
        

    def clear_all(self):
        self.got_tables = False
        self.clear_canvas()
        self.clear_tables()

    def clear_tables(self):
        self.got_tables = False
        empty_df1 = pd.DataFrame()
        empty_model1 = DataFrameModel(empty_df1)

        self.h1_tableView.setModel(empty_model1)
        self.h2_tableView.setModel(empty_model1)
        self.h1_result_tableView.setModel(empty_model1)
        self.h2_result_tableView.setModel(empty_model1)

    def show_error_box(self, str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(str)
        msg.setWindowTitle("Error")
        msg.exec_()

    def show_ok_box(self, str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Ok")
        msg.setInformativeText(str)
        msg.setWindowTitle("Ok")
        msg.exec_()

    def check_settings(self):
        self.func = create_func(self.diff_eq_func_line_edit.text())
        
        if isinstance(self.func, str):
            self.settings_norm = False
            self.activate_plot_buttons(False)
            self.show_error_box("Неправильный синтаксис для функции дифференциального уравнения. " + self.func)
            return 

        for le in self.get_diff_eq_line_edits():
            if not le.text().strip():
                self.activate_plot_buttons(False)
                self.show_error_box("Заполните все параметры для дифференциального уравнения")
                return


        if self.use_actual_solution_checkBox.isChecked() == True:
            self.sol = create_func(self.diff_eq_solution_line_edit.text())
            if isinstance(self.sol, str):
                self.settings_norm = False
                self.activate_plot_buttons(False)
                self.show_error_box("Неправильный синтаксис для функции точного решения. " + self.sol)
                self.sol = None
                return

            for le in self.get_solution_line_edits():
                if not le.text().strip():
                    self.activate_plot_buttons(False)
                    self.show_error_box("Заполните все параметры для точного решения дифференциального уравнения")
                    return
            self.read_solution_values()
        

        self.settings_norm = True            
        self.activate_plot_buttons(True)

        if self.use_actual_solution_checkBox.isChecked() == False:
            self.actual_solution_btn.setDisabled(True)

        self.read_diff_eq_values()
        self.show_ok_box("Настройки подтверждены!")

    def read_diff_eq_values(self):
        x0 = self.x0_le.text()
        y0 = self.y0_le.text()

        diff_eq_a  = self.diff_eq_a_le.text()
        diff_eq_b  = self.diff_eq_b_le.text()
        diff_eq_h1 = self.diff_eq_h1_le.text()
        diff_eq_h2 = self.diff_eq_h2_le.text()

        self.x0 = str_to_float(x0)
        self.y0 = str_to_float(y0)

        self.diff_eq_a  = str_to_float(diff_eq_a)
        self.diff_eq_b  = str_to_float(diff_eq_b)
        self.diff_eq_h1 = str_to_float(diff_eq_h1)
        self.diff_eq_h2 = str_to_float(diff_eq_h2)

    def read_solution_values(self):
        solution_a = self.solution_a_le.text() 
        solution_b = self.solution_b_le.text() 
        solution_h = self.solution_h_le.text() 

        self.solution_a = str_to_float(solution_a)
        self.solution_b = str_to_float(solution_b) 
        self.solution_h = str_to_float(solution_h)
        

    def activate_plot_buttons(self, state):
        state = not state
        self.Runge_Kutta_method_btn.setDisabled(state)
        self.Eulers_method_btn.setDisabled(state)
        self.Eulers_Cauchy_method_btn.setDisabled(state) 
        self.midpoint_method_btn.setDisabled(state) 
        self.actual_solution_btn.setDisabled(state) 
        
    def clear_canvas(self):
        self.figure.clear()
        self.canvas.draw()

    def plot_actual_solution(self):
        # a, b = self.diff_eq_a, self.diff_eq_b
        # actual_x = np.arange(a, b, self.solution_h)
        # actual_y = [self.sol(i) for i in actual_x]
        x0, y0 = self.x0, self.y0

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.set_xlabel("X")  # обозначаем оси
        ax.set_ylabel("Y")
        sol_str = self.diff_eq_solution_line_edit.text().replace("**", "^")
        ax.set_title(f"Точное аналитическое решение\ny = {sol_str}\ny({x0})={y0}")
        # ax.plot(actual_x, actual_y, label="Аналитическое решение")
        self.plot_actual_solution_on_exist(ax)
        ax.legend()
        ax.grid()  
        self.canvas.draw()

    def plot_actual_solution_on_exist(self, ax):
        if self.use_actual_solution_checkBox.isChecked() == True:
            if self.sol != None and not isinstance(self.sol, str):
                actual_x = np.arange(self.solution_a, self.solution_b, self.solution_h)
                actual_y = [self.sol(i) for i in actual_x]
                ax.plot(actual_x, actual_y, label="Аналитическое решение")

    def plot_midpoint_method(self):
        a, b = self.diff_eq_a, self.diff_eq_b
        x0, y0 = self.x0, self.y0
        h1, h2 = self.diff_eq_h1, self.diff_eq_h2

        df = midpoint_method(self.func, x0, y0, a, b, h1, self.sol)
        df2 = midpoint_method(self.func, x0, y0, a, b, h2, self.sol)

        self.set_tables(df, df2)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.set_xlabel("X")  # обозначаем оси
        ax.set_ylabel("Y")
        diff_eq_str = self.diff_eq_func_line_edit.text().replace("**", "^")
        ax.set_title(f"Задача Коши методом средней точки\ny' = {diff_eq_str}\ny({x0})={y0}")
        ax.plot(df.xi, df.yi, label=f"h={h1}")  # строим 
        ax.plot(df2.xi, df2.yi, label=f"h={h2}") # графики
        self.plot_actual_solution_on_exist(ax)
        ax.scatter(df.xi, df.yi)  # отмечаем узловые точки
        ax.scatter(df2.xi, df2.yi, label="узловые точки")
        ax.legend()
        ax.grid()  
        self.canvas.draw()

    def plot_Runge_Kutta(self):
        a, b = self.diff_eq_a, self.diff_eq_b
        x0, y0 = self.x0, self.y0
        h1, h2 = self.diff_eq_h1, self.diff_eq_h2
        
        x1 = np.arange(a, b+h1, h1)
        x2 = np.arange(a, b+h2, h2)
        df1, y1 = Runge_Kutte_method(self.func, x0, y0, a, b+h1, h1, self.sol)
        df2, y2 = Runge_Kutte_method(self.func, x0, y0, a, b+h2, h2, self.sol)
        y1.pop(), y2.pop()

        self.set_tables(df1, df2)
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.set_xlabel("X")  # обозначаем оси
        ax.set_ylabel("Y")
        diff_eq_str = self.diff_eq_func_line_edit.text().replace("**", "^")
        ax.set_title(f"Задача Коши методом Рунге-Кутты\ny' = {diff_eq_str}\ny({x0})={y0}")
        ax.plot(x1, y1, label=f"h={h1}")  # строим 
        ax.plot(x2, y2, label=f"h={h2}") # графики
        self.plot_actual_solution_on_exist(ax)
        ax.scatter(x1, y1)  # отмечаем узловые точки
        ax.scatter(x2, y2, label="узловые точки")
        ax.legend()
        ax.grid()  # сохраняем изображение
        self.canvas.draw()

    def plot_Euler_Cauchy_method(self):
        a, b = self.diff_eq_a, self.diff_eq_b
        x0, y0 = self.x0, self.y0
        h1, h2 = self.diff_eq_h1, self.diff_eq_h2

        df = Euler_Cauchy_method(self.func, x0, y0, a, b, h1, self.sol)
        df2 = Euler_Cauchy_method(self.func, x0, y0, a, b, h2, self.sol)

        self.set_tables(df, df2)

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        diff_eq_str = self.diff_eq_func_line_edit.text().replace("**", "^")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title(f"Задача Коши методом Эйлера-Коши\ny' = {diff_eq_str}\ny({x0})={y0}")
        ax.plot(df.xi, df.yi, label=f"h={h1}")  # строим 
        ax.plot(df2.xi, df2.yi, label=f"h={h2}") # графики
        self.plot_actual_solution_on_exist(ax)
        ax.scatter(df.xi, df.yi)  # отмечаем узловые точки
        ax.scatter(df2.xi, df2.yi, label="узловые точки")
        ax.legend()
        ax.grid()  
        self.canvas.draw()

    def plot_Euler_method(self):
        a, b = self.diff_eq_a, self.diff_eq_b
        x0, y0 = self.x0, self.y0
        h1, h2 = self.diff_eq_h1, self.diff_eq_h2

        df = Eulers_method(self.func, x0, y0, a, b, h1, self.sol)
        df2 = Eulers_method(self.func, x0, y0, a, b, h2, self.sol)

        self.set_tables(df, df2)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.set_xlabel("X")  # обозначаем оси
        ax.set_ylabel("Y")
        diff_eq_str = self.diff_eq_func_line_edit.text().replace("**", "^")
        ax.set_title(f"Задача Коши явным методом Эйлера\ny' = {diff_eq_str}\ny({x0})={y0}")
        ax.plot(df.xi, df.yi, label=f"h={h1}")  # строим 
        ax.plot(df2.xi, df2.yi, label=f"h={h2}") # графики
        self.plot_actual_solution_on_exist(ax)
        ax.scatter(df.xi, df.yi)  # отмечаем узловые точки
        ax.scatter(df2.xi, df2.yi, label="узловые точки")
        ax.legend()
        ax.grid()
        self.canvas.draw()

    def set_tables(self, df1, df2):
        pd.set_option('precision', 3)

        h1_res = df1[["xi", "yi"]]
        h2_res = df2[["xi", "yi"]]

        self.curr_all_h1 = df1
        self.curr_all_h2 = df2
        self.curr_res_h1 = h1_res
        self.curr_res_h2 = h2_res
        self.got_tables = True

        h1_model = DataFrameModel(df1)
        h2_model = DataFrameModel(df2)
        h1_res_model = DataFrameModel(h1_res)        
        h2_res_model = DataFrameModel(h2_res)

        self.h1_tableView.setModel(h1_model)
        self.h2_tableView.setModel(h2_model)
        self.h1_result_tableView.setModel(h1_res_model)
        self.h2_result_tableView.setModel(h2_res_model)

        self.h1_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.h2_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.h1_result_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.h2_result_tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        self.h1_tableView.resizeColumnsToContents()
        self.h2_tableView.resizeColumnsToContents()
        self.h1_result_tableView.resizeColumnsToContents()
        self.h2_result_tableView.resizeColumnsToContents()

    def save_prepare(self):
        btn_clicked = self.sender()
        btn_name = btn_clicked.objectName()
        df_to_save = None
        filename = ""

        if "save_all_h1" in btn_name:
            filename = "Таблица_расчётов_h=1.csv"
            df_to_save = self.curr_all_h1
        elif "save_all_h2" in btn_name:
            filename = "Таблица_расчётов_h=2.csv"
            df_to_save = self.curr_all_h2
        elif "save_res_h1" in btn_name:
            filename = "Таблица_результатов_h=1.csv"
            df_to_save = self.curr_res_h1
        elif "save_res_h2" in btn_name:
            filename = "Таблица_результатов_h=2.csv"
            df_to_save = self.curr_res_h2

        self.save_table(df_to_save, filename)

    def save_table(self, df, filename):
        if self.got_tables:
            actual_filename = getFileNameToSave(self, filename)
            if actual_filename:
                df.to_csv(actual_filename, float_format='%1.5f', sep=";")
        else:
            self.nothing_to_save_msg()

    def nothing_to_save_msg(self):
        self.show_ok_box("Нет данных для сохранения")
            
    def upload_data_from_file(self):
        fileName = getFileNameToOpen(self)
        if not fileName:
            return 

        try:
            basic_data = read_data(fileName, 
              ["y_func", "x0", "y0", "diff_eq_a", "diff_eq_b", "diff_eq_h1", "diff_eq_h2", 
                    "y_sol", "sol_a", "sol_b", "sol_h"])

        except Exception as e:
            self.show_error_box("Ошибка при чтении файла: " + str(e))
            return 

        try:
            self.diff_eq_func_line_edit.setText(basic_data['y_func'][0])
            self.x0_le.setText(basic_data['x0'][0])
            self.y0_le.setText(basic_data['y0'][0])
            self.diff_eq_a_le.setText(basic_data['diff_eq_a'][0])
            self.diff_eq_b_le.setText(basic_data['diff_eq_b'][0])
            self.diff_eq_h1_le.setText(basic_data['diff_eq_h1'][0])
            self.diff_eq_h2_le.setText(basic_data['diff_eq_h2'][0])

            try:
                self.diff_eq_solution_line_edit.setText(basic_data['y_sol'][0])
                self.solution_a_le.setText(basic_data['sol_a'][0])
                self.solution_b_le.setText(basic_data['sol_b'][0])
                self.solution_h_le.setText(basic_data['sol_h'][0])
            except Exception as e:
                self.show_ok_box("Невозможно прочитать данные для аналитической функции: " + str(e))

        except Exception as e:
            self.show_error_box("Ошибка при заполнении данных: " + str(e))
        
        

    def switch(self):
        self.switch_window.emit("from diff equation window")