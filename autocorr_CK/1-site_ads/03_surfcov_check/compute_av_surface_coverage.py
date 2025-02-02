import numpy as np
import os
import json
import math
from plot_surfcov import plot_surfcov

skipfac = 0.25      # this factor determines how many initial steps will be discarded 
gen_plot = True     # whether to generate a plot for the time profile of the average surf coverage
nindcurves = 1      # number of curves included for individual runs. If < 1, no curves are included.

logdir = "../" + sorted(d for d in os.listdir("..") if d.startswith("log"))[-1]
resdir = "../" + sorted(d for d in os.listdir("..") if d.startswith("res"))[-1]

# Read input variables from the JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
total_sites = var_data["xhi"] * var_data["yhi"]

nskiprows = int(skipfac*Nstep)

# Initialize an array to store average coverage for each run
mean_surfcov_per_run = np.zeros(Nruns)
var_surfcov_per_run = np.zeros(Nruns)

for i in range(1, Nruns+1):
    # Load coverage data for each run
    surfcov = np.loadtxt(os.path.join(resdir, "surfcov{}.txt".format(i)), skiprows=nskiprows)[:, 1]
    
    # Calculate and store the mean coverage for this run
    mean_surfcov_per_run[i-1] = np.mean(surfcov) 

    # Calculate and store the variance of coverage for this run
    var_surfcov_per_run[i-1] = np.var(surfcov,ddof=1) 

mean1 = np.mean(mean_surfcov_per_run)
std1 = math.sqrt(np.var(mean_surfcov_per_run,ddof=1)/Nruns)
mean2 = np.mean(var_surfcov_per_run)
std2 = math.sqrt(np.var(var_surfcov_per_run,ddof=1)/Nruns)

# Calculate theoretical results for 1-site adsorption
ra = 2*ra2
rd = 2*rd2
mean_coverage_analytic = ra / (ra + rd)
variance_coverage_analytic = (ra * rd) / ((ra + rd)**2 * total_sites)

# Print results for mean and var 
print("\nComparing theoretical and simulation results (skipfac=%f, Nruns=%d)" % (skipfac,Nruns))
print("1. Mean Surface Coverage:")
print("   Theory:   %e" % mean_coverage_analytic)
print("   Simulation: %e (std err=%e)" % (mean1,std1))

print("\n2. Variance of Surface Coverage:")
print("   Theory:   %e" % variance_coverage_analytic)
print("   Simulation: %e (std err=%e)" % (mean2,std2))

# plot
if gen_plot: 
    print("\nGenerating a plot for surf coverage...")
    plot_surfcov(resdir,total_sites,nindcurves)
