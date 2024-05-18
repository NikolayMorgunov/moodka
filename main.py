import numpy as np
from rk4 import rk4
from draw_plot import draw_2d
from numpy.linalg import norm, inv
from Params import Params
from f import f
from scipy.spatial.transform import Rotation
import magnetic_field
from control import magnetic_control, ideal_control

J = np.eye(3)
J[0] *= 2
J[1] *= 3
J[2] *= 4

InclinedDipole = True  # False if is Straight
params = Params(J=J, mu=3.986e14, Rev=6378.1e3, J2=1.082e-3, mu_e=7.812e15, field_mode='straight',
                control_mode='magnetic',)
                # coils=np.array([[1, 0, 0],
                #                 [0, 1, 0],
                #                 [0, 0, 1]]))

# Euler angles
psi = 0
theta = 0
phi = 0
rot = Rotation.from_euler('zxz', [psi, theta, phi])

w0 = np.array([0.2, 0.3, 0.5])

r0 = np.array([7e6, 0, 0])
norm_v = np.sqrt(params.mu/norm(r0))
inc = np.pi/3
v0 = np.array([0, norm_v*np.sin(inc), norm_v*np.cos(inc)])
x0 = np.concatenate([[psi, theta, phi], w0])
T = 7200
h = 0.1

t = np.arange(0, T, h)
n = np.size(t)

h_control = 0.2
n_control_cur = int(h_control / h)

X = np.zeros((13, n))  # 0:4 кватернион, 4:7 относительная угловая скорость, 7:13 rv вектор
X[:, 0] = np.concatenate([rot.as_quat(), w0, r0, v0])

X_quat2euler = np.zeros((3, n))
X_quat2euler[:, 0] = Rotation.from_quat(X[:, 0][:4]).as_euler('zxz')

w_if = np.zeros((3, n))
w_if[:, 0] = Rotation.from_quat(X[:, 0][:4]).apply(X[4:7, 0], inverse=False)

B_last_bf = magnetic_field.magnetometer(0, X[:, 0], params)
print_ticks = 0
for i in range(n - 1):
    tau = h * i  # current time

    if not (i % n_control_cur):
        B_bf = magnetic_field.magnetometer(tau, X[:, i], params)

        if params.control_mode == 'ideal':
            u = ideal_control(tau, X[:, i], B_bf, params)
        else:
            u = magnetic_control(tau, X[:, i], h_control, B_last_bf, B_bf, params)
            B_last_bf = np.copy(B_bf)

    X[:, i + 1] = rk4(tau, X[:, i], u, f, h, params)
    X[:, i + 1][:4] /= norm(X[:, i + 1][:4])
    X_quat2euler[:, i + 1] = Rotation.from_quat(X[:, i + 1][:4]).as_euler('zxz')
    w_if[:, i + 1] = Rotation.from_quat(X[:4, i + 1]).apply(X[4:7, i + 1], inverse=False)

    if (i / n) >= print_ticks * 0.01:
        print(print_ticks)
        print_ticks += 1

        print('psi =', X_quat2euler[0, i])
        print('theta =', X_quat2euler[1, i])
        print('phi =', X_quat2euler[2, i])
        print('w =', X[:, i][4:7])
        # print('K_ssk =', K_ssk[:, i])
        print()
        if params.field_mode == 'straight':
            print('B_str =', magnetic_field.dipole(tau, X[:, i], params))
        else:
            print('B_inc =', magnetic_field.dipole(tau, X[:, i], params))
        print('I = ', u)
        print()

draw_2d(t, X_quat2euler[0], 'plots/psi quat.html', xlabel='t, s', name='psi quat')
draw_2d(t, X_quat2euler[1], 'plots/theta quat.html', xlabel='t, s', name='theta quat')
draw_2d(t, X_quat2euler[2], 'plots/phi quat.html', xlabel='t, s', name='phi quat')

fig = draw_2d(t, X[4], 'plots/w.html', xlabel='t, s', name='wx')
draw_2d(t, X[5], 'plots/w.html', xlabel='t, s', name='wy', fig=fig)
draw_2d(t, X[6], 'plots/w.html', xlabel='t, s', name='wz', fig=fig)

fig = draw_2d(t, w_if[0], 'plots/w_if.html', xlabel='t, s', name='w_if_x')
draw_2d(t, w_if[1], 'plots/w_if.html', xlabel='t, s', name='w_if_y', fig=fig)
draw_2d(t, w_if[2], 'plots/w_if.html', xlabel='t, s', name='w_if_z', fig=fig)
