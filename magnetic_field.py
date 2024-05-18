import numpy as np
from numpy.linalg import norm
from scipy.spatial.transform import Rotation


def dipole(t, x, params):
    rv = x[7:13]

    if params.field_mode == 'straight':
        k = np.array([0, 0, -1])
    else:
        omega_e = 2 * np.pi / 86400

        delta = 168 / 180 * np.pi
        lmbd = -70 / 180 * np.pi + omega_e * t
        k = np.array([np.cos(lmbd) * np.sin(delta),
                      np.sin(lmbd) * np.sin(delta),
                      np.cos(delta)])

    r = rv[:3]
    abs_r = norm(r)
    B = -params.mu_e / abs_r ** 5 * (abs_r ** 2 * k - 3 * r * (k @ r))

    return B


def magnetometer(t, x, params):
    B_if_real = dipole(t, x, params)

    B_bf_real = Rotation.from_quat(x[:4]).apply(B_if_real, inverse=True)
    B_bf_got = params.G @ B_bf_real + np.random.normal(0, 200e-9, 3)

    return B_bf_got
