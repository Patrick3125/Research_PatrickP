import numpy as np
import os
import json
import math

logdir = "../log"
resdir = "../res"

# Read input variables from the JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
skip = int(Nstep/4)
Nstep -= skip-1  

rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
total_sites = var_data["xhi"] * var_data["yhi"] * 2

theta = 1 / (1 + math.sqrt(rd2 / ra2))

# Initialize an array to store average coverage for each run
average_cov_per_run = np.zeros(Nruns)

for i in range(1, Nruns+1):
    # Load coverage data for each run
    coverage = np.loadtxt(os.path.join(resdir, "data{}.txt".format(i)), skiprows=skip)[:, 1]
    
    # Calculate the average coverage for this run and normalize by total sites
    run_average_cov = np.mean(coverage) / total_sites
    
    # Store the average coverage for this run
    average_cov_per_run[i-1] = run_average_cov

print("theta = " + str(theta))

# Save the average surface coverage for each run to a file
# This will create a file with Nruns rows and one column, each row corresponding to the average coverage for a run
np.savetxt(os.path.join(resdir, "average_surface_coverage.txt"), average_cov_per_run, fmt="%f", header="av_surface_cov_per_run")

# If you still need to save theta, you can save it separately or append it to the file as needed.
np.savetxt(os.path.join(resdir, "theta.txt"), np.array([[np.mean(average_cov_per_run), theta]]), fmt="%f %f", header="average_cov_all_runs, theta")
