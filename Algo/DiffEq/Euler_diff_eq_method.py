"""
Функции для численного решения
задачи Коши для обыкновенного дифференциального
уравнения явным методом Эйлера

    * Eulers_method - метод Эйлера

Автор: Шнайдер Антон
"""

# библиотека для построение графиков
import matplotlib.pyplot as plt  
import numpy as np  # для работы с массивами
import pandas as pd # для работы с табличными данными 
from dataclasses import make_dataclass
# для создания классов данных 


def Eulers_method(func, x0, y0, a, b, h, sol=None):
    """
    Euler's numerical method
    for solving differential equation
    with initial condition x0, y0
    on the interval [a; b]
    """

    Iteration = make_dataclass("Iteration", 
                    [
                        ("xi", float), 
                        ("yi", float), 
                        ("delta_yi", float),
                        ("actual_yi", float),
                        ("eps", float)
                    ])

    # создаём таблицу и
    # заполняем первую строку таблицы начальными значениями
    diff = 0
    if sol != None:
        diff = abs(y0 - sol(x0))
    df = pd.DataFrame([Iteration(x0, y0, 0, func(x0), 
                        diff)])
    
    # получаем иксы на интервале [a;b+h]
    # с шагом h
    x = np.arange(a, b+h, h)

    i = 1
    # начинаем итерироваться со второго элемента
    for xi in x[i:]:
        # получаем предыдущие значения x и y
        # из таблицы 
        y_prev = df.iloc[i-1]["yi"]
        x_prev = df.iloc[i-1]["xi"]

        # вычисляем правуб часть ДУ f(x, y)
        fi = func(x_prev, y_prev)
        delta_y = h * fi  # получаем дельта у
        yi = y_prev + delta_y  # получаем новый игрек

        # вычисляем настоящее аналитическое
        # значение решения в точке xi
        actual_y = 0
        if sol != None:
            actual_y = sol(xi)

        # добавляем в таблицу новую строку с данными
        df = df.append([Iteration(xi, yi, delta_y, actual_y, abs(actual_y - yi))], 
                            ignore_index=True)
        i += 1

    return df  # возвращаем таблицу
    
