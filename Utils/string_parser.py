from math import *
import math
import sys

def create_eval_str(str):
    new_str = str.replace('^', '**')
    return new_str

def create_func(str):
    x = 0.00001
    y = 0.0000001
    z = 0.0000000001 
    try:
        eval(str)
    except Exception as e:
        return f"error: {e}"
        
    def func(x=0, y=0, z=0):
        return eval(str)
        
    return func

def str_to_float(str):
    return float(str.replace(',', '.'))



    