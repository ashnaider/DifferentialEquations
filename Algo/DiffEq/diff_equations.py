import math

def f(x, y):
    """ 
    rigth part f(x, y) of 
    y' = f(x, y) differential equation type

    diff eq: y' = (y + x)^2
    right part: (y + x)^2
    """
    return (y + x)**2 

def diff_eq_solution(x):
    """ 
    analitical solution: y = tg(x) - x 
    of y' = (y + x)^2 diff equation
    """
    return math.tan(x) - x 
