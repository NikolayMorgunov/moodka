import numpy as np
from numpy.linalg import inv, norm


class Params:
    def __init__(self, J=None, m=None, l=None, mu=None, Rev=None, J2=None, mu_e=None, field_mode=None,
                 control_mode=None, coils=np.eye(3)):
        self.J = J
        self.inv_J = inv(J)
        self.m = m
        self.g = 9.81
        self.l = l
        self.mu = mu
        self.Rev = Rev
        self.J2 = J2
        self.mu_e = mu_e
        self.k = 1e7
        self.field_mode = field_mode
        self.control_mode = control_mode
        self.coils = coils
        e1_real = np.array([1, 0, 0]) + np.random.normal(0, np.sin(np.pi / 180), 3)
        e1_real /= norm(e1_real)

        e2_real = np.array([0, 1, 0]) + np.random.normal(0, np.sin(np.pi / 180), 3)
        e2_real /= norm(e2_real)

        e3_real = np.array([0, 0, 1]) + np.random.normal(0, np.sin(np.pi / 180), 3)
        e3_real /= norm(e3_real)

        self.G = np.array([e1_real, e2_real, e3_real])
