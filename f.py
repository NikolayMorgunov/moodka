import numpy as np
from numpy.linalg import norm, inv
from scipy.spatial.transform import Rotation
from rotation.quat_mult import quat_mult
import magnetic_field


# орбитальное движение, угловое движение с учетом гравитационного и магнитного моментов и управления
def f(t, x, u, params):
    q = x[:4]
    w = x[4:7]
    r = x[7:10]
    v = x[10:]

    w_quat = np.concatenate([w, [0]])

    J = params.J

    dq = quat_mult(q, w_quat) / 2

    # гравитационный момент

    rot = Rotation.from_quat(q)

    Rc = rot.apply(r, inverse=True)
    abs_Rc = norm(Rc)
    E3 = Rc / abs_Rc

    M_grav = 3 * params.mu / abs_Rc ** 3 * np.cross(E3, J @ E3)  # гравитационный момент

    B_if = magnetic_field.dipole(t, x, params)

    B_bf = rot.apply(B_if, inverse=True)

    M_mag = np.cross(params.coils @ u, B_bf)  # магнитный момент

    dw = np.matmul(params.inv_J, -np.cross(w, np.matmul(J, w)) + M_grav + M_mag)

    abs_r = norm(r)
    dr = v

    dv_grav = -params.mu * r / abs_r ** 3
    delta = 3 / 2 * params.J2 * params.mu * params.Rev ** 2
    dv_j2 = delta * (r * (-1 / abs_r ** 5 + 5 * r[2] ** 2 / abs_r ** 7) +
                     np.array([0, 0, -2 * r[2] / abs_r ** 5]))

    dv = dv_grav + dv_j2
    return np.concatenate([dq, dw, dr, dv])
