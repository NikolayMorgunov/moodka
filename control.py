import numpy as np
from numpy.linalg import inv


def magnetic_control(t, x, h, B_last_bf, B_cur_bf, params):
    B_dot = (B_cur_bf - B_last_bf) / h

    m = -params.k * B_dot

    n_coils = params.coils[0].size
    F = params.coils
    I = F.T @ inv(F @ F.T) @ m

    for i in range(n_coils):
        if abs(I[i]) > 50.:
            I[i] /= abs(I[i]) * 50.

    return I


def ideal_control(t, x, B_bf, params):
    w = x[4:7]
    B_dot = np.cross(B_bf, w)

    m = -params.k * B_dot

    return m
