import numpy as np
import math
import sys
import os
import json

def autocorr(x, max_lag):

    mean = np.mean(x)
    fluctuations = x - mean
    
    N = len(fluctuations)
    
    # Initialize array for acf
    correlations = np.zeros(max_lag)
    
    # Calculate correlation for each tau
    for tau in range(max_lag):
        correlation_sum = 0
        for t in range(N - tau):  
            correlation_sum += fluctuations[t] * fluctuations[t + tau]
        
        correlations[tau] = correlation_sum / (N-tau)
    
    return correlations

if len(sys.argv) != 5:
    print("Usage: python compute_correlation.py <input_res_file> <output_file> <logdir> <resdir>")
    sys.exit(1)

input_res_file = sys.argv[1]
output_file = sys.argv[2]
logdir = sys.argv[3]
resdir = sys.argv[4]

# Read input variables from json file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"] * var_data["yhi"]
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]
average_cov = np.loadtxt(os.path.join(resdir, "theta.txt"), skiprows=1)[1]

# cut off the first 100 steps, and then maxtau will be 90% of that (temporory hardcoded for 150)
maxtau = 150

x_values = []
y_values = []
with open(input_res_file, "r") as f:
    #cut off first few lines
    lines = f.readlines()[300:]
    for line in lines:
        x_values.append(float(line.split()[0]))
        y_values.append(float(line.split()[1]) / total_sites)

new_values = np.array(y_values)

# autocorr function is at top
corrs = autocorr(new_values, maxtau)

time_points = np.array(range(maxtau)) * deltat

# Save the data
individual_data_to_save = np.column_stack((time_points, corrs))
np.savetxt(output_file, individual_data_to_save, fmt="%.8f %.8f", header="time correlation")
