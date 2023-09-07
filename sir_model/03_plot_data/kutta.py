import numpy as np
import matplotlib.pyplot as plt

def diff_equations(y, t, b, k):
    s, i, r = y
    ds_dt = -b*s*i
    di_dt = b*s*i - k*i
    dr_dt = k*i
    return np.array([ds_dt, di_dt, dr_dt])

def runge_kutta(func, y0, t, args=()):
    dt = t[1] - t[0]
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        k1 = dt * np.array(func(y[i], t[i], *args))
        k2 = dt * np.array(func(y[i] + k1 / 2., t[i] + dt / 2., *args))
        k3 = dt * np.array(func(y[i] + k2 / 2., t[i] + dt / 2., *args))
        k4 = dt * np.array(func(y[i] + k3, t[i] + dt, *args))
        y[i + 1] = y[i] + 1 / 6. * (k1 + 2 * k2 + 2 * k3 + k4)
    return y

# Set the parameters
b = 0.43
k = 0.3
t = np.arange(0, 150, 0.05)

# initial conditions
y0 = np.array([1, 0.0008, 0])

sir = runge_kutta(diff_equations, y0, t, args=(b, k))

# plot the results
plt.figure(figsize=(12,6))
plt.plot(t, sir[:, 0], label='S(t)')
plt.plot(t, sir[:, 1], label='I(t)')
plt.plot(t, sir[:, 2], label='R(t)')
plt.xlabel('Time')
plt.ylabel('Population fraction')
plt.legend()
plt.savefig('a_kutta.png') # save the figure
plt.show()
