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
Nstep -= 100

rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
total_sites = var_data["xhi"] * var_data["yhi"]

theta = 1 / (1 + math.sqrt(rd2 / ra2))


average_cov = np.zeros(Nstep)
for i in range(1, Nruns+1):
    coverage = np.loadtxt(os.path.join(resdir, "data{}.txt".format(i)), skiprows=101)[:, 1]
    average_cov += np.array(coverage)

average_cov /= Nruns
average_cov /= total_sites

print("average surface coverage = " + str(np.mean(average_cov)) + ", theta = " + str(theta))

# Save the average surface coverate and theta to a file
data_to_save = np.column_stack((np.loadtxt(os.path.join(resdir, "data1.txt"), skiprows=101)[:, 0], average_cov))
np.savetxt(os.path.join(resdir, "average_surface_coverage.txt"), data_to_save, fmt="%f %f", header="time av_surface_cov")

np.savetxt(os.path.join(resdir, "theta.txt"), np.column_stack((np.mean(average_cov), theta)), fmt="%f %f", header="average_cov_all, theta")

