import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import LogLocator, LogFormatter, AutoLocator


# Path where the files are stored
resdir = "../res"

# detect the number of correlation data files
correlation_files = [f for f in os.listdir(resdir) if f.startswith('corr')]
num_files = len(correlation_files)

# Read the saved average correlation data
data = np.loadtxt(os.path.join(resdir, "average_corr.txt"))
tau_values = data[:, 0]
average_corrs = data[:, 1]
variances = data[:, 2]

fig, ax = plt.subplots()

# Plot each individual correlation data
for i in range(1, num_files + 1):
    try:
        individual_data = np.loadtxt(os.path.join(resdir, "corr{}.txt".format(i)))
        individual_corrs = individual_data[:, 1]
        ax.plot(tau_values, individual_corrs, '-', color='lightblue', alpha=0.2, linewidth=1)
    except IOError:
        print("corr{}.txt not found. Skipping...".format(i))

ax.plot(1, 1, '-', color='lightblue', alpha=0.2, linewidth=1, label = "individual correlation")


# Plot the average correlations
ax.plot(tau_values, average_corrs, '-', color='blue', linewidth=2, label="Average Correlation")

#zoom into average
ax.set_xlim([np.min(tau_values) , np.max(tau_values)])
ax.set_ylim([np.min(average_corrs) * 0.8, np.max(average_corrs) * 1.2])

x0 = np.mean(tau_values)
y0 = average_corrs[np.argmin(np.abs(tau_values - x0))]

def log_log_line(x, m, x0, y0):
    return y0 * (x / x0)**m

y_neg1 = log_log_line(tau_values, -1, x0, y0)
y_neg0_5 = log_log_line(tau_values, -0.5, x0, y0)
y_neg1_5 = log_log_line(tau_values, -1.5, x0, y0)

ax.plot(tau_values, y_neg1, 'r--', label='Slope -1')
ax.plot(tau_values, y_neg0_5, 'g--', label='Slope -0.5')
ax.plot(tau_values, y_neg1_5, 'm--', label='Slope -1.5')

#log scale
plt.xscale("log")
plt.yscale("log")

ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('')
ax.grid(False)
ax.legend(loc='upper right')

plt.show()

