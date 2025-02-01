import numpy as np
import os
import json
import sys
logdir = sys.argv[1]
resdir = sys.argv[2]
# Read input variables from the JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]
maxtau = 150
all_corrs = np.zeros(shape = (Nruns, maxtau))
average_corrs = np.zeros(maxtau)
for i in range(0, Nruns):
    corrs = np.loadtxt(os.path.join(resdir, "corr{}.txt".format(i+1)))[:, 1]
    all_corrs[i]=corrs
    average_corrs += np.array(corrs)
#calculate average
average_corrs /= Nruns


standard_errors=np.zeros(maxtau)
# Calculate the variance for each point
for tau in range(0, maxtau):
    corr_values = all_corrs[:,tau]  
    corr_mean = sum(corr_values) / len(corr_values)
    sample_variance = sum((x - corr_mean) ** 2 for x in corr_values) / (len(corr_values) - 1)
    standard_error = ((sample_variance / len(corr_values)) ** 0.5)
    standard_errors[tau] = standard_error

data_to_save = np.column_stack((np.arange(1, maxtau+1), average_corrs, standard_errors))
np.savetxt(os.path.join(resdir, "average_corr.txt"), data_to_save, fmt="%d %.8f %.8f", 
           header="# Nruns = {}\n# deltat = {}\n# tau average_acf standard error".format(Nruns, deltat))
