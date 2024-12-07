import numpy as np


def bisection(f, a, b, epsilon):
    if f(a) * f(b) > 0:
        print("Error: Function does not change sign in the interval.")
        return None
    while (b - a) / 2 > epsilon:
        c = (a + b) / 2
        if abs(f(c)) < epsilon:
            return c
        elif f(a) * f(c) < 0:
            b = c
        else:
            a = c

    return (a + b) / 2


def golden_section(f, a, b, epsilon):
    gr = (np.sqrt(5) + 1) / 2
    while b - a > epsilon:
        y_1 = b - (b - a) / gr
        y_2 = a + (b - a) / gr
        if f(y_1) < f(y_2):
            b = y_2
        else:
            a = y_1
    x_min = (a + b) / 2
    return x_min, f(x_min)


def gradient_ascent(df, f, x0, alpha, N):
    x = x0
    for _ in range(N):
        x = x + alpha * df(x)
    return x, f(x)
