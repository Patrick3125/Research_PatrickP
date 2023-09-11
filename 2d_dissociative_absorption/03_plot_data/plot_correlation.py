import matplotlib.pyplot as plt
import numpy as np
import os

# Path where the files are stored
path = "../02_parse_compute/"

# Automatically detect the number of correlation data files
correlation_files = [f for f in os.listdir(path) if f.startswith('correlation_data_log')]
num_files = len(correlation_files)

# Read the saved average correlation data
data = np.loadtxt(os.path.join(path, "correlation_data.txt"))
i_values = data[:, 0]
average_corrs = data[:, 1]
variances = data[:, 2]

fig, ax = plt.subplots()

# Plot each individual correlation data
for i in range(1, num_files + 1):
    try:
        individual_data = np.loadtxt(os.path.join(path, f"correlation_data_log{i}.txt"))
        individual_corrs = individual_data[:, 1]
        ax.plot(i_values, individual_corrs, '-', color='lightblue', alpha=0.2, linewidth=1)
    except FileNotFoundError:
        print(f"correlation_data_log{i}.txt not found. Skipping...")

# Plot the average correlations
ax.plot(i_values, average_corrs, '-', color='blue', linewidth=2, label="Average Correlation")

# Plot the error bars at an interval
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(i_values[::errbar_interval],
            average_corrs[::errbar_interval],
            yerr=np.sqrt(variances[::errbar_interval]),
            fmt='', ecolor='red')

ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('Graphs from log files')
ax.grid(True)
ax.legend(loc='upper right')

plt.show()

