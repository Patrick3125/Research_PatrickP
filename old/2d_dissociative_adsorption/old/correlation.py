import numpy as np
import math
import sys
import os
import json
import re

logdir = "../log"
resdir = "../res"
corrdir = "../correlation"

# Create the folder to save computed data if it doesn't exist
if not os.path.exists(corrdir):
    os.makedirs(corrdir)

#read input variables from json file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"] * var_data["yhi"]
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]


maxtau = int(min(Nstep * 0.9, 100000))  #maxtau will be set to 90% of Nstep, 250 maximum
theta = 1 / (1 + math.sqrt(rd2 / ra2))

# initialize arrays
all_corrs = []
average_corrs = np.zeros(maxtau - 1)
variances = np.zeros(maxtau - 1)

#find log files
res_files = [f for f in os.listdir(resdir) if f.startswith('res') and f.endswith('.txt')]



# Loop through all log files
for i in range(1, Nruns+1):
    x_values = []
    y_values = []
    filename = os.path.join(resdir, "res{}.txt".format(i))

    with open(filename, "r") as f:
        lines = f.readlines()
        
        for line in lines:

            x_values.append(float(line.split()[0]))
            y_values.append(float(line.split()[1]) / total_sites)

    corrs = []
    new_values = np.array(y_values)
    new_values -= theta
    for tau in range(1, maxtau):
        new_x = new_values[:-tau]
        new_y = new_values[tau:]
        corrs.append(np.correlate(new_x, new_y, mode='valid')[0])

    #save individual conrrelations
    individual_data_to_save = np.column_stack((range(1, maxtau), corrs))
    np.savetxt(os.path.join(corrdir, "correlation{}.txt".format(i)), individual_data_to_save, fmt="%d %f", header="i correlation")
    all_corrs.append(corrs)
    average_corrs += np.array(corrs)


average_corrs /= Nruns


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
np.savetxt(os.path.join(corrdir, "average_correlation.txt"), data_to_save, fmt="%d %f %f", header="i average_correlation variance")
print("Finished writing correlation.txt files in ../correlations")
