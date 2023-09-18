import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
import os
import sys

# Automatically detect the number of log files
log_folder = "../01_run_sir/"
log_files = [f for f in os.listdir(log_folder) if f.startswith('log') and f.endswith('.spparks')]
num_files = len(log_files)
#size will be read from file.
size = 1

print("detected number of files : " + str(num_files))

all_s = []
all_i = []
all_r = []
Trun = float(sys.argv[4])
runtime = float(sys.argv[5])
x_val = np.arange(0, runtime * Trun + Trun, Trun)
# Loop through all log files
for i in range(1, num_files+1):
    s_val = []
    i_val = []
    r_val = []
    filename = os.path.join(log_folder, "log{}.spparks".format(i))

    with open(filename, "r") as f:
        lines = f.readlines()[105:]

        start_from = False
        last_line_before_loop = None

        for line in lines:
            if "- nreaction = 0" in line or  "Naccept" in line:
                start_from = True
                continue
            if start_from and line.split()[0] == "Loop":
                start_from = False
                if last_line_before_loop is not None:
                    s_val.append(float(last_line_before_loop.split()[6]) / size)
                    i_val.append(float(last_line_before_loop.split()[7]) / size)
                    r_val.append(float(last_line_before_loop.split()[8]) / size)
                continue
            if start_from:
                last_line_before_loop = line
                if float(line.split()[0]) == 0:
                    size = float(line.split()[6]) + float(line.split()[7]) + float(line.split()[8])
                    s_val.append(float(line.split()[6]) / size)
                    i_val.append(float(line.split()[7]) / size)
                    r_val.append(float(line.split()[8]) / size)

    all_s.append(s_val)
    all_i.append(i_val)
    all_r.append(r_val)
average_s = np.mean(np.array(all_s), axis=0)
average_i = np.mean(np.array(all_i), axis=0)
average_r = np.mean(np.array(all_r), axis=0)


def deriv(y, t, b, f):
    S, I, R = y
    dSdt = -b * S * I
    dIdt = b * S * I - f * I
    dRdt = f * I
    return dSdt, dIdt, dRdt

# Define RK4 method
def rk4(func, y0, t, args=()):
    dt = t[1] - t[0]
    y = np.zeros((len(t), len(y0)))
    y[0] = y0
    for i in range(len(t) - 1):
        k1 = np.array(func(y[i], t[i], *args))
        k2 = np.array(func(y[i] + dt * k1 / 2., t[i] + dt / 2., *args))
        k3 = np.array(func(y[i] + dt * k2 / 2., t[i] + dt / 2., *args))
        k4 = np.array(func(y[i] + dt * k3, t[i] + dt, *args))
        y[i + 1] = y[i] + dt * 1 / 6. * (k1 + 2 * k2 + 2 * k3 + k4)
    return y
# Define the objective function
def objective(params):
    b, f = params
    y0 = [average_s[0], average_i[0], average_r[0]]
    sol = rk4(deriv, y0, x_val, args=(b, f))
    #Mean Squared Error
    mse = np.mean((sol[:, 0] - average_s) ** 2 + ((sol[:, 1] - average_i) ** 2) + (sol[:, 2] - average_r) ** 2)
    return mse
# Optimize
#initial_guess = [0.6, 0.3]
#solution = minimize(objective, initial_guess, method='Nelder-Mead', options={'xatol': 1e-8, 'disp': True})
#b, f = solution.x
bounds = [(0, 1.2), (0, 1)]
result = differential_evolution(objective, bounds)
b, k = result.x
print("input values: It = ", sys.argv[1], ", Rt = ", sys.argv[2], ", diffrate = ", sys.argv[3])
print("Optimized parameters: b = ", b, ", f = ", k)

#save the individual trajectories
for i in range(num_files):
    data = np.column_stack((x_val, all_s[i], all_i[i], all_r[i]))
    np.savetxt("../sir_indiv" + str(i) + ".txt", data, fmt="%f %f %f %f", header="x s i r")

#save the graphs from mean squared error method
y0=[average_s[0], average_i[0], average_r[0]]        
data = rk4(deriv, y0 , x_val, args=(b, k))
np.savetxt("../sir_ode.txt", data, fmt="%f %f %f", header="ODE for: s i r")

#save the graphs from contact number method
s_inf = average_s[-1]
c = np.log(s_inf)/(s_inf-1)
k_2 = float(sys.argv[2])
b_2 = c * k_2
data = rk4(deriv, y0 , x_val, args=(b_2, k_2))
np.savetxt("../sir_contact.txt", data, fmt="%f %f %f", header="ODE for: s i r")

#save the params
with open('../ode_params.txt', 'ab') as f:
    np.savetxt(f, np.column_stack((float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), b, k, b_2, k_2)), fmt="%f %f %f %f %f %f %f",header = "It, Rt, diffrate, b, k, b2, k2")



#save the averages
data_to_save = np.column_stack((x_val, average_s, average_i, average_r))
np.savetxt("../sir_averages.txt", data_to_save, fmt="%f %f %f %f", header="x average_s average_i average_r")

