"""
Функции для численного решения
задачи Коши для обыкновенного дифференциального
уравнения методом Рунге-Кутты
а также построение графиков

    * Runge_Kutte_method - метод Рунге-Кутты

Автор: Шнайдер Антон
"""

# библиотека для построение графиков
import matplotlib.pyplot as plt  
import numpy as np  # для работы с массивами
import pandas as pd
from dataclasses import make_dataclass


def Runge_Kutte_method(f, x0, y0, a, b, h, sol=None):
    x = np.arange(a, b, h)

    Iteration = make_dataclass("Iteration", 
                    [
                        ("i_v", str),
                        ("xi", float), 
                        ("ri", float),
                        ("delta_yi", float),
                        ("yi", float), 
                        ("actual_yi", float),
                        ("eps", float)
                    ])

    actual_y, eps = None, None
    if sol != None:
        actual_y = sol(x0)
        eps = abs(y0 - actual_y)
    df = pd.DataFrame()
    
    res = [y0]
    y_prev = y0
    actual_y, eps = None, None
    if sol != None:
        actual_y = sol(x0)
        eps = abs(y0 - actual_y)
    i = 0
    for xi in x:
        r1 = h * f(xi, y_prev)
        r2 = h * f(xi + h/2, y_prev + r1/2)
        r3 = h * f(xi + h/2, y_prev + r2/2)
        r4 = h * f(xi + h, y_prev + r3)

        delta_y = 1/6 * (r1 + 2*r2 + 2*r3 + r4)

        actual_y, eps = None, None
        if sol != None:
            actual_y = sol(xi)
            eps = abs(y_prev - actual_y)

        df = df.append([Iteration(f"{i}/1", xi,       r1, None,    y_prev, actual_y, eps)], ignore_index=True)
        df = df.append([Iteration(f"{i}/2", xi + h/2, r2, None,    y_prev, actual_y, eps)], ignore_index=True)
        df = df.append([Iteration(f"{i}/3", xi + h/2, r3, None,    y_prev, actual_y, eps)], ignore_index=True)
        df = df.append([Iteration(f"{i}/4", xi + h,   r4, delta_y, y_prev, actual_y, eps)], ignore_index=True)

        yi = y_prev + delta_y
        y_prev = yi
        res.append(yi)
        i += 1

    return df, res


