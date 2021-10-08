"""
Функции для численного решения
задачи Коши для обыкновенного дифференциального
уравнения методом средней точки

    * midpoint_method - метод Эйлера - Коши

Автор: Шнайдер Антон
"""

# библиотека для построение графиков
import matplotlib.pyplot as plt  
import numpy as np  # для работы с массивами
import pandas as pd # для работы с табличными данными 
from dataclasses import make_dataclass
# для создания классов данных 


def midpoint_method(f, x0, y0, a, b, h, sol=None):
    """Задача Коши методом средней точки"""
    Iteration = make_dataclass("Iteration", 
                    [
                        ("xi", float), 
                        ("yi", float), 
                        ("yi_sq", float),
                        ("delta_yi", float),
                        ("actual_yi", float),
                        ("eps", float)
                    ])
    # создаём таблицу и
    # заполняем первую строку таблицы начальными значениями
    actual_y, eps = None, None
    if sol != None:
        actual_y = sol(x0)
        eps = abs(y0 - actual_y)
    df = pd.DataFrame([Iteration(x0, y0, 0, 0, actual_y, 
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

        xi_sq = x_prev + h / 2.0  # получаем х и у с волной
        yi_sq = y_prev + (h / 2.0) * f(x_prev, y_prev)

        delta_y = h * f(xi_sq, yi_sq) # вычисляем дельта игрек
        yi = yi_sq + delta_y  # получаем игрек для текущего узла

        # точное значение аналитического решения
        actual_y, eps = None, None
        if sol != None:
            actual_y = sol(xi)
            eps = abs(yi - actual_y)
        
        # добавляем в таблицу новую строку
        df = df.append([Iteration(xi, yi, yi_sq, delta_y, actual_y, eps)], ignore_index=True)
        i+=1
    
    # print(df, "\n")  # печатаем таблицу
    return df  # возвращаем таблицу

