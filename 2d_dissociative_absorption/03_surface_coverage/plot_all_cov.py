import matplotlib.pyplot as plt
import numpy as np
import json
import os

# Path where the files are stored
logdir = "../log"
resdir = "../res"

with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)
total_sites = var_data["xhi"] * var_data["yhi"]
Nruns = var_data["Nruns"]


# Detect the number of correlation data files
data_files = [f for f in os.listdir(resdir) if f.startswith('data')]
num_files = len(data_files)

# Read the saved average correlation data
data = np.loadtxt(os.path.join(resdir, "average_surface_coverage.txt"))
time = data[:, 0]
average_cov = data[:, 1]

data = np.loadtxt(os.path.join(resdir, "theta.txt"), skiprows=1)
theta = data[1]



fig, ax = plt.subplots()
all_cov = []
# Plot each individual correlation data
for i in range(1, num_files + 1):
    try:
        individual_data = np.loadtxt(os.path.join(resdir, "data{}.txt".format(i)))
        individual_cov = individual_data[:, 1]/total_sites
        individual_time = individual_data[:, 0]
        
        all_cov.append(np.loadtxt(os.path.join(resdir, "data{}.txt".format(i)), skiprows=101 )[:, 1]/total_sites)
        ax.plot(individual_time, individual_cov, '-', color='lightblue', alpha=1, linewidth=1)
    except IOError:
        print("data{}.txt not found. Skipping...".format(i))


variances = np.zeros(len(time))

# Calculate the variance for each point
for t in range(0, len(time)):
    mean_value = average_cov[t]
    #only calculate variance when num_files is more than one
    if (Nruns > 1):
        variance = sum((np.array([corrs[t] for corrs in all_cov]) - mean_value)**2) / (Nruns - 1)
        variances[t] = variance
    else:
        variances[t] = 0


# Plot the average correlations
ax.plot(time, average_cov, '-', color='green', linewidth=2, label="Average Coverage", zorder=4)

# Plot the error bars at an interval
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(time[::errbar_interval],
            average_cov[::errbar_interval],
            yerr=np.sqrt(variances[::errbar_interval]),
            fmt='', ecolor='red', zorder=3)

#ax.axhline(y=np.mean(average_cov), color='purple', linestyle='--', label='Mean of Average Coverage')
ax.axhline(y=theta, color='purple', linestyle='--', label='theta')

ax.legend(loc="lower right")
ax.set_xlabel('time')
ax.set_ylabel('coverage')
ax.set_title('')
ax.grid(True)

plt.show()


