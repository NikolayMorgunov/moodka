import numpy as np


def rk4(t0, x0, u, f, h, params):
    k1 = f(t0, x0, u, params)
    k2 = f(t0 + h / 2, x0 + h / 2 * k1, u, params)
    k3 = f(t0 + h / 2, x0 + h / 2 * k2, u, params)
    k4 = f(t0 + h, x0 + h * k3, u, params)

    x1 = x0 + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)

    return x1
