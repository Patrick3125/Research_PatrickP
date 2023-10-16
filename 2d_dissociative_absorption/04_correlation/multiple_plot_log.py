import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import LogLocator, LogFormatter, AutoLocator
from matplotlib import cm

# Path where the files are stored
base_dir = ".."

fig, ax = plt.subplots()
allaverage = []
# Loop through each directory and plot data with different colors
for i in range(1, 11):
    resdir = os.path.join(base_dir, "res_{}".format(i*100))

    # detect the number of correlation data files
    correlation_files = [f for f in os.listdir(resdir) if f.startswith('corr')]
    num_files = len(correlation_files)

    # Read the saved average correlation data
    data = np.loadtxt(os.path.join(resdir, "average_corr.txt"))
    tau_values = data[:, 0]
    average_corrs = data[:, 1]
    variances = data[:, 2]

    allaverage.append( average_corrs);

    # Choose a color from the gradient
    color = cm.jet((i-1)/10.0)

    # Plot the average correlations
    ax.plot(tau_values, average_corrs, '-', color=color, linewidth=2, label="size = {}^2".format(i*100))

ax.set_xlim([np.min(tau_values), np.max(tau_values)])
ax.set_ylim([np.min(allaverage) * 0.8, np.max(allaverage) * 1.2])

x0 = np.mean(tau_values)
y0 = average_corrs[np.argmin(np.abs(tau_values - x0))]

y_neg1 = y0 * (tau_values / x0)**-1
y_neg0_5 = y0 * (tau_values / x0)**-0.5
#y_neg1_5 = y0 * (tau_values / x0)**-1.5

ax.plot(tau_values, y_neg1, 'r--', label='Slope -1')
ax.plot(tau_values, y_neg0_5, 'g--', label='Slope -0.5')
#ax.plot(tau_values, y_neg1_5, 'm--', label='Slope -1.5')

# log scale
plt.xscale("log")
plt.yscale("log")

ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('')
ax.grid(False)
ax.legend(loc='upper right')
fig.savefig('../temp_graph/all.png')
plt.show()

