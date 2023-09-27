import numpy as np
import os
import json

logdir = "../log"
corrdir = "../correlation"

# Ensure the directory exists
if not os.path.exists(corrdir):
    os.makedirs(corrdir)

# Read input variables from the JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
maxtau = int(min(Nstep * 0.9, 100000))

# Read all correlations once and store in a list
all_corrs = [np.loadtxt(os.path.join(corrdir, "correlation" + str(i) + ".txt"))[:, 1] for i in range(1, Nruns + 1)]

# Calculate the average correlations
average_corrs = np.mean(all_corrs, axis=0)

# Calculate the variance for each point

variances = []
if Nruns > 1:
    for tau in range(maxtau - 1):
        mean_value = average_corrs[tau]
        variance = sum([(corrs[tau] - mean_value)**2 for corrs in all_corrs]) / (Nruns - 1)
        variances.append(variance)
else:
    variances = np.zeros(maxtau - 1)

# Save the average_corrs and variances to a file
data_to_save = np.column_stack((range(1, maxtau), average_corrs, variances))
np.savetxt(os.path.join(corrdir, "average_correlation.txt"), data_to_save, fmt="%d %f %f", header="i average_correlation variance")
print("Finished writing average_correlation.txt file in {}".format(corrdir))

