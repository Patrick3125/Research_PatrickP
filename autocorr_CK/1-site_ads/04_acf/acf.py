import numpy as np
import math
import os
import sys
import json
import glob

def theory_acf_1site_ads(t,ra,rd,nsite):
    return ra*rd/(ra+rd)**2/nsite*math.exp(-(ra+rd)*t)

#########################
# acf computing routine #
#########################

def compute_acf(x,max_lag):

    Npt = len(x)
    if Npt<=max_lag:
        print("Error: max_lag is too big")
        sys.exit(0)

    mean = np.mean(x)
    deltax = x - mean

    acf = np.zeros(max_lag+1)
    for tau in range(max_lag+1):
        tmp = 0.0
        for t in range(Npt-tau):
            tmp += deltax[t]*deltax[t+tau]
        acf[tau] = tmp/(Npt-tau)

    return acf

#########################
# changeable parameters #
#########################

logdir = "../log"           # directory of sim_params.txt (input)
resdir = "../res"           # directory of surfcov files (input) and output files

outfile = "res.acf"         # output filename for main results (time vs. acf)
max_lag = 100               # compute acf up to t = max_lag*dt
nskiptpt = 1000             # discard this many initial timepoints when computing acf

###################
# before we start #
###################

# read simulation parameters from the JSON file
with open(os.path.join(logdir,'sim_params.txt')) as f:
    var_data = json.load(f)

Nrun = var_data["Nrun"]
Nstep = var_data["Nstep"]
ra = var_data["ra"]
rd = var_data["rd"]
xhi = var_data["xhi"] 
yhi = var_data["yhi"]
dt = var_data["deltat"]

# compute needed variables
nsite = xhi*yhi

######################
# read surfcov files #
######################

# get the list of all surfcov files and sort them
surfcov_files = sorted(glob.glob(os.path.join(resdir,'surfcov*.txt')))
if not surfcov_files:
    print("no surfcov files found in %s" % resdir)
    os.exit(0) 
print("\n%d surfcov files found in %s" % (len(surfcov_files),resdir))

# check the number of surfcov files
if not Nrun==len(surfcov_files):
    print("Nrun=%d but there are %d surfcov files in %s" % (Nrun,len(surfcov_files),resdir))
    sys.exit(0) 

# check the number of time points in each file
first_data = np.loadtxt(surfcov_files[0])
tpts = first_data[:,0]
if not Nstep==len(tpts): 
    print("Nstep=%d but there are %d time points in %s" % (Nstep,len(tpts),surfcov_files[0])) 
    sys.exit(0) 

# read surfcov / compute and store acf
all_acf = np.zeros((Nrun,max_lag+1))
for i, surfcov_file in enumerate(surfcov_files):
    data = np.loadtxt(surfcov_file)
    surfcov = data[nskiptpt:,1]
    acf = compute_acf(surfcov,max_lag)
    all_acf[i] = acf

#############################################
# computee the average acf and standard err #
#############################################

mean_acf = np.mean(all_acf,axis=0)
var_acf = np.var(all_acf,ddof=1,axis=0)
stderr_acf = np.sqrt(var_acf/Nrun)

###########################
# compute theoretical acf #
###########################

tpts = dt*np.arange(max_lag+1)
theo_acf = np.zeros(max_lag+1)
for i in range(max_lag+1):
    theo_acf[i] = theory_acf_1site_ads(tpts[i],ra,rd,nsite)

####################
# data file output #
####################

fullpath_outfile=os.path.join(resdir,outfile)
np.savetxt(fullpath_outfile,np.column_stack([tpts,mean_acf,stderr_acf,theo_acf]),header="time\tsim_acf\tstd_err\ttheo_acf")
print("\ndata file saved as %s" % fullpath_outfile)
