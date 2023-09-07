import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

def parse_logfile(filename):
    time, spec1, spec2, spec3 = [], [], [], []

    with open(filename, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if "Time" in line:
            start_index = lines.index(line) + 1
            break

    for line in lines[start_index:]:
        if not line.split()[0].replace('.','',1).isdigit():  
            break

        data = line.split()
        time.append(float(data[0]))
        spec1.append(float(data[6]))
        spec2.append(float(data[7]))
        spec3.append(float(data[8]))

    return time, spec1, spec2, spec3

def interpolate_to_common_time(time, spec, common_time):
    interpolation_function = interp1d(time, spec, fill_value="extrapolate")
    return interpolation_function(common_time)

common_time = np.unique(np.concatenate([parse_logfile('log{}.spparks'.format(seed))[0] for seed in range(1, 11)]))

spec1_avg = np.zeros_like(common_time)
spec2_avg = np.zeros_like(common_time)
spec3_avg = np.zeros_like(common_time)

count = 0

for seed in range(1, 11):
    time, spec1, spec2, spec3 = parse_logfile('log{}.spparks'.format(seed))

    total_population = np.array(spec1)[0] + np.array(spec2)[0] + np.array(spec3)[0]

    spec1 = interpolate_to_common_time(time, np.array(spec1)/total_population, common_time)
    spec2 = interpolate_to_common_time(time, np.array(spec2)/total_population, common_time)
    spec3 = interpolate_to_common_time(time, np.array(spec3)/total_population, common_time)

    if spec2[-1] == 0:
        plt.plot(common_time, spec1, 'bo', alpha=0.002, markersize=1, color='lightblue')
        plt.plot(common_time, spec2, 'ro', alpha=0.002, markersize=1, color='lightcoral')
        plt.plot(common_time, spec3, 'go', alpha=0.002, markersize=1, color='lightgreen')

    else:
        spec1_avg += spec1
        spec2_avg += spec2
        spec3_avg += spec3
        count += 1
        plt.plot(common_time, spec1, 'bo', alpha=0.002, markersize=1)
        plt.plot(common_time, spec2, 'ro', alpha=0.002, markersize=1)
        plt.plot(common_time, spec3, 'go', alpha=0.002, markersize=1)

spec1_avg /= count
spec2_avg /= count
spec3_avg /= count

plt.plot(common_time, spec1_avg, 'b-', label='Average Susceptible')
plt.plot(common_time, spec2_avg, 'r-', label='Average Infected')
plt.plot(common_time, spec3_avg, 'g-', label='Average Recovered')

def diff_equations(params, t, y):
    b, f = params
    s, i, r = y
    ds_dt = -b * s * i
    di_dt = b * s * i - f * i
    dr_dt = f * i
    return np.array([ds_dt, di_dt, dr_dt])

def runge_kutta(params, s_0, i_0, r_0, t):
    dt = t[1] - t[0]
    y = np.empty((len(t), 3))
    y[0] = np.array([s_0, i_0, r_0])

    for i in range(len(t) - 1):
        k1 = dt * diff_equations(params, t[i], y[i])
        k2 = dt * diff_equations(params, t[i] + dt/2, y[i] + k1/2)
        k3 = dt * diff_equations(params, t[i] + dt/2, y[i] + k2/2)
        k4 = dt * diff_equations(params, t[i] + dt, y[i] + k3)
        y[i+1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6

    return y[:, 0], y[:, 1], y[:, 2]  # return S, I, R

params = np.array([0.8, 0.7])  # initial parameters
lr = 0.001  # learning rate
iterations = 100  # number of training iterations
min_param_value = 0.00001  # minimum allowed parameter value
max_param_value = 100  # maximum allowed parameter value

for i in range(iterations):
    # Calculate prediction with current parameters
    s_pred, i_pred, r_pred = runge_kutta(params, spec1_avg[0], spec2_avg[0], spec3_avg[0], common_time)

    # Calculate error
    diff_s = spec1_avg - s_pred
    diff_i = spec2_avg - i_pred
    diff_r = spec3_avg - r_pred
    error = np.sum(diff_s**2) + np.sum(diff_i**2) + np.sum(diff_r**2)

    # Calculate gradients
    grad_b = -2 * np.sum(diff_s * (-i_pred * spec1_avg) + diff_i * (spec1_avg * i_pred - spec2_avg))
    grad_f = -2 * np.sum(diff_i * spec2_avg + diff_r * spec3_avg)

    # Update the parameters
    params[0] -= lr * grad_b
    params[1] -= lr * grad_f

    # Clip the parameters to avoid them getting too high or too low
    params = np.clip(params, min_param_value, max_param_value)

    # Print progress
    if i % 10 == 0:
        print("Iteration %s: params = %s, error = %s" % (i, params, error))

# Print final parameters
print(params)

s_final, i_final, r_final = runge_kutta(params, spec1_avg[0], spec2_avg[0], spec3_avg[0], common_time)

plt.plot(common_time, s_final, 'b--', label='Predicted Susceptible')
plt.plot(common_time, i_final, 'r--', label='Predicted Infected')
plt.plot(common_time, r_final, 'g--', label='Predicted Recovered')

plt.xlabel('Time')
plt.ylabel('Quantity')
plt.title('Quantity of Spec1 and Spec2 Over Time')
plt.legend()
plt.grid(True)
plt.savefig("a_graph.png")
plt.show()
