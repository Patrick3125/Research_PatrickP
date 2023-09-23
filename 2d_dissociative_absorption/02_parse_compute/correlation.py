import numpy as np
import math
import sys
import os
import json
import re

logdir = "../log"
datadir = "../log/computed_data"

# Create the folder to save computed data if it doesn't exist
if not os.path.exists(datadir):
    os.makedirs(datadir)

#read input variables from json file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"] * var_data["yhi"]
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]

print("Total of " + str(Nruns) + " log files detected.")

maxtau = int(min(Nstep * 0.9, 100000))  #maxtau will be set to 90% of Nstep, 250 maximum
theta = 1 / (1 + math.sqrt(rd2 / ra2))

# initialize arrays
all_corrs = []
average_corrs = np.zeros(maxtau - 1)
variances = np.zeros(maxtau - 1)

#find log files
log_files = [f for f in os.listdir(logdir) if f.startswith('log') and f.endswith('.spparks')]



# Loop through all log files
for i in range(1, Nruns+1):
    x_values = []
    y_values = []
    filename = os.path.join(logdir, "log{}.spparks".format(i))

    with open(filename, "r") as f:
        lines = f.readlines()
        
        previous_line_is_data = False
        save_previous_line = None

        for line in lines:

            #only read second line when there are two lines after each other
        
            # Used Regular expressions to find lines with only 7 numbers
            real_data = re.match(r"\s*([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)", line)
            
            if real_data:
                if previous_line_is_data:
                    x_values.append(float(real_data.group(1)))
                    y_values.append(float(real_data.group(7)) / total_sites)
                    previous_line_is_data = False
                else:
                    previous_line_is_data = True
                    save_previous_line = real_data
            elif previous_line_is_data:
                x_values.append(float(save_previous_line.group(1)))
                y_values.append(float(save_previous_line.group(7)) / total_sites)
                previous_line_is_data = False

    corrs = []
    new_values = np.array(y_values)
    new_values -= theta
    for tau in range(1, maxtau):
        new_x = new_values[:-tau]
        new_y = new_values[tau:]
        #corrs.append(np.correlate(new_x, new_y, mode='valid')[0])
        corrs.append(np.corrcoef(new_x, new_y)[0, 1])

    #save individual conrrelations
    individual_data_to_save = np.column_stack((range(1, maxtau), corrs))
    np.savetxt(os.path.join(datadir, "correlation{}.txt".format(i)), individual_data_to_save, fmt="%d %f", header="i correlation")
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
np.savetxt(os.path.join(datadir, "average_correlation.txt"), data_to_save, fmt="%d %f %f", header="i average_correlation variance")
print("Finished writing correlation.txt files in ../log/computed_data")
