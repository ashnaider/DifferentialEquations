"""
Функции для численного решения
задачи Коши для обыкновенного дифференциального
уравнения методом Эйлера-Коши

    * Euler_Cauchy_method - метод Эйлера - Коши

Автор: Шнайдер Антон
"""

# библиотека для построение графиков
import matplotlib.pyplot as plt  
import numpy as np  # для работы с массивами
import pandas as pd # для работы с табличными данными 
from dataclasses import make_dataclass
# для создания классов данных 


def Euler_Cauchy_method(func, x0, y0, a, b, h, sol=None):
    # создаём таблицу и
    # заполняем первую строку таблицы начальными значениями

    Iteration = make_dataclass("Iteration", 
                    [
                        ("xi", float), 
                        ("yi", float), 
                        ("yi_sq", float),
                        ("delta_yi", float),
                        ("actual_yi", float),
                        ("eps", float)
                    ])

    eps, solution = None, None
    if sol != None:
        solution = sol(x0)
        eps = abs(y0 - solution)
        
    df = pd.DataFrame([Iteration(x0, y0, 0, 0, solution, 
                        eps)])
    
    # получаем иксы на интервале [a;b+h]
    # с шагом h
    x = np.arange(a, b+h, h)

    i = 1
    for xi in x[i:]:
        # получаем предыдущие значения x и y
        # из таблицы 
        y_prev = df.iloc[i-1]["yi"]
        x_prev = df.iloc[i-1]["xi"]

        # вычисляем правую часть ДУ f(x, y)
        fi = func(x_prev, y_prev)
        yi_sq = y_prev + h * fi  # получаем игрек с волной

        # вычисляем дельта игрек
        delta_y = 0.5 * h * (func(x_prev, y_prev) + func(xi, yi_sq))
        yi = y_prev + delta_y  # получаем игрек для i-й точки

        # точное аналитическое знаачение
        actual_y, eps = None, None
        if sol != None:
            actual_y = sol(xi)
            eps = abs(actual_y - yi)

        df = df.append([Iteration(xi, yi, yi_sq, delta_y, actual_y, eps)], 
                                                ignore_index=True)
        i+=1

    return df  # возвращаем таблицу

