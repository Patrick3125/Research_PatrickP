import numpy as np
import os
import json

logdir = "../log"
resdir = "../res"

# Read input variables from the JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
maxtau = int((Nstep - 100) * 0.9)

all_corrs = []
average_corrs = np.zeros(maxtau-1)
for i in range(1, Nruns+1):
    corrs = np.loadtxt(os.path.join(resdir, "corr{}.txt".format(i)))[:, 1]
    all_corrs.append(corrs)
    average_corrs += np.array(corrs)

#calculate average
average_corrs /= Nruns

variances = np.zeros(maxtau - 1)

# Calculate the variance for each point
for tau in range(maxtau - 1):
    mean_value = average_corrs[tau]
    #only calculate variance when num_files is more than one
    if (Nruns > 1):
        variance = sum((np.array([corrs[tau] for corrs in all_corrs]) - mean_value)**2) / (Nruns - 1)
        variances[tau] = variance
    else:
        variances[tau] = 0

# Save the average_corrs and variances to a file
data_to_save = np.column_stack((range(1, maxtau), average_corrs, variances))
np.savetxt(os.path.join(resdir, "average_corr.txt"), data_to_save, fmt="%d %f %f", header="i average_correlation variance")

