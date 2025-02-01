import numpy as np
import os
import json
import math
logdir = "../" + sorted(d for d in os.listdir("..") if d.startswith("log_"))[-1]
resdir = "../" + sorted(d for d in os.listdir("..") if d.startswith("res_"))[-1]

# Read input variables from the JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
skip = int(Nstep/4) # only use the last qurter
Nstep -= skip-1 
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
total_sites = var_data["xhi"] * var_data["yhi"]
theta = 1 / (1 + math.sqrt(rd2 / ra2))
# Initialize an array to store average coverage for each run
average_cov_per_run = np.zeros(Nruns)

# Modified: Store all time trajectories to calculate variance correctly
all_trajectories = []

for i in range(1, Nruns+1):
    # Load coverage data for each run
    coverage = np.loadtxt(os.path.join(resdir, "data{}.txt".format(i)), skiprows=skip)[:, 1]
    
    # Normalize coverage by total sites
    normalized_coverage = coverage / total_sites
    
    # Store the normalized trajectory
    all_trajectories.append(normalized_coverage)
    
    # Calculate the average coverage for this run
    run_average_cov = np.mean(normalized_coverage)
    
    # Store the average coverage for this run
    average_cov_per_run[i-1] = run_average_cov

print("theta = " + str(theta))

# Calculate mean surface coverage from simulation
mean_coverage_sim = np.mean(average_cov_per_run)

# Convert trajectories to numpy array for easier calculation
all_trajectories = np.array(all_trajectories)
all_data = all_trajectories.flatten()

# Calculate variance using explicit formula
mean_value = np.mean(all_data)
squared_diff_sum = np.sum((all_data - mean_value)**2)
N = len(all_data)
variance_coverage_sim = squared_diff_sum / (N - 1)

# Calculate analytical results
ra = ra2
rd = rd2
mean_coverage_analytic = ra / (ra + rd)
variance_coverage_analytic = (ra * rd) / ((ra + rd)**2 * total_sites)

# Print results and comparison
print("\nResults Comparison:")
print("1. Mean Surface Coverage:")
print("   Simulation: %.8f" % mean_coverage_sim)
print("   Analytic:   %.8f" % mean_coverage_analytic)

print("\n2. Variance of Surface Coverage:")
print("   Simulation: %.8f" % variance_coverage_sim)
print("   Analytic:   %.8f" % variance_coverage_analytic)
# Save the average surface coverage for each run to a file
# This will create a file with Nruns rows and one column, each row corresponding to the average coverage for a run
np.savetxt(os.path.join(resdir, "average_surface_coverage.txt"), average_cov_per_run, fmt="%f", header="av_surface_cov_per_run")

# If you still need to save theta, you can save it separately or append it to the file as needed.
np.savetxt(os.path.join(resdir, "theta.txt"), np.array([[np.mean(average_cov_per_run), theta]]), fmt="%f %f", header="average_cov_all_runs, theta")

