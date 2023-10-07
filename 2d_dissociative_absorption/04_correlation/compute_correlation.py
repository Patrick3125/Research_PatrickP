import numpy as np
import math
import sys
import os
import json

if len(sys.argv) != 3:
    print("Usage: python compute_correlation.py <input_res_file> <output_file>")
    sys.exit(1)

input_res_file = sys.argv[1]
output_file = sys.argv[2]

logdir = "../log"

# Read input variables from json file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"] * var_data["yhi"]
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]

# cut off the first 100 steps, and then maxtau will be 90% of that
maxtau = int(min((Nstep-100) * 0.9, 250))
theta = 1 / (1 + math.sqrt(rd2 / ra2))

x_values = []
y_values = []

with open(input_res_file, "r") as f:
    #cut off first 100 lines
    lines = f.readlines()[100:]
    for line in lines:
        x_values.append(float(line.split()[0]))
        y_values.append(float(line.split()[1]) / total_sites)

corrs = []
new_values = np.array(y_values)
new_values -= theta

#calculate correlation for each tau
for tau in range(1, maxtau):
    new_x = new_values[:-tau]
    new_y = new_values[tau:]
    corrs.append(np.correlate(new_x, new_y, mode='valid')[0])

# Save individual correlations
individual_data_to_save = np.column_stack((range(1, maxtau), corrs))
np.savetxt(output_file, individual_data_to_save, fmt="%d %f", header="i correlation")


