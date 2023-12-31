import matplotlib.pyplot as plt
import numpy as np
import os

# Path where the files are stored
resdir = "../res"

# Detect the number of correlation data files
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


# Plot the average correlations
ax.plot(tau_values, average_corrs, '-', color='green', linewidth=2, label="Average Correlation")

# Plot the error bars at an interval
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(tau_values[::errbar_interval],
            average_corrs[::errbar_interval],
            yerr=np.sqrt(variances[::errbar_interval]),
            fmt='', ecolor='red', zorder=3)

ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('')
ax.grid(True)
ax.legend(loc='upper right')

plt.show()

