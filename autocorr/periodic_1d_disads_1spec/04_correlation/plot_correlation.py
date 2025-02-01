import matplotlib.pyplot as plt
import numpy as np
import os
import json
import math

logdir = "../log_1000"
resdir = "../res_1000"

with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
ra2 = var_data["ra2"]
rd2 = var_data["rd2"]


# Read the number of runs from the header
with open(os.path.join(resdir, "average_corr.txt"), 'r') as f:
    header = f.readline()  # Read first line
    Nruns = int(header.split('=')[1].split('\n')[0].strip())  # Extract Nruns value

# Detect the number of correlation data files
correlation_files = [f for f in os.listdir(resdir) if f.startswith('corr')]
num_files = len(correlation_files)

# Read the saved average correlation data
data = np.loadtxt(os.path.join(resdir, "average_corr.txt"))
tau_values = data[:, 0] * 0.01 
average_corrs = data[:, 1]
variances = data[:, 2]

# Calculate standard error from variance and N
standard_errors = np.sqrt(variances/Nruns)

fig, ax = plt.subplots()

# Plot each individual correlation data
for i in range(1, num_files + 1):
    try:
        individual_data = np.loadtxt(os.path.join(resdir, "corr{}.txt".format(i)))
        individual_corrs = individual_data[:, 1]
        ax.plot(tau_values, individual_corrs, '-', color='lightblue', alpha=0.2, linewidth=1)
    except IOError:
        print("corr{}.txt not found. Skipping...".format(i))

# Plot the average correlations
ax.plot(tau_values, average_corrs, '-', color='green', linewidth=2, label="Average Correlation")

# Plot the error bars at an interval using standard error
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(tau_values[::errbar_interval],
            average_corrs[::errbar_interval],
            yerr=standard_errors[::errbar_interval],  # Using standard error instead of sqrt(variance)
            fmt='', ecolor='red', zorder=3)
ax.plot(tau_values,[ (1/float(Nruns) * rd2*ra2/(rd2+ra2) * math.exp(-1*(ra2+rd2)*i)) for i in tau_values ], color='blue', label="Analytical")

ax.set_xlabel('tau * dt')
ax.set_ylabel('correlation')
ax.set_title('')
ax.grid(True)
ax.legend(loc='upper right')
plt.savefig('correlation_plot', dpi=300, bbox_inches='tight')
plt.show()
