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

def compute_acf_old(x,max_lag):

    Npt = len(x)
    if Npt<=max_lag:
        print("Error: max_lag is too big")
        sys.exit(0)

    mean = np.mean(x)
    deltax = x-mean

    acf = np.zeros(max_lag+1)
    for tau in range(max_lag+1):
        tmp = 0.0
        for t in range(Npt-tau):
            tmp += deltax[t]*deltax[t+tau]
        acf[tau] = tmp/(Npt-tau)

    return acf

def compute_acf(x,max_lag):

    Npt = len(x)
    if Npt<=max_lag:
        print("Error: max_lag is too big")
        sys.exit(0)

    mean = np.mean(x)
    deltax = x-mean

    acf = np.zeros(max_lag+1)
    for tau in range(max_lag+1):
        tmp = 0.0
        deltax1 = deltax[:Npt-tau]
        deltax2 = deltax[tau:Npt]
        tmp = np.dot(deltax1,deltax2)    
        acf[tau] = tmp/(Npt-tau)

    return acf

def compute_ccf(x, y, max_lag):
    Npt_x = len(x)
    Npt_y = len(y)
    
    if Npt_x != Npt_y:
        print("Error: x and y must have the same length")
        sys.exit(0)

    Npt = Npt_x #lengths are equal.
    if Npt <= max_lag:
        print("Error: max_lag is too big")
        sys.exit(0)

    mean_x = np.mean(x)
    mean_y = np.mean(y)
    deltax = x - mean_x
    deltay = y - mean_y

    ccf = np.zeros(max_lag + 1)
    for tau in range(max_lag + 1):
        deltax1 = deltax[:Npt - tau]
        deltay2 = deltay[tau:Npt]
        tmp = np.dot(deltax1, deltay2)
        ccf[tau] = tmp / (Npt - tau)

    return ccf

#########################
# changeable parameters #
#########################

logdir = "../log"           # directory of sim_params.txt (input)
resdir = "../res"           # directory of surfcov files (input) and output files

outfile = "res.acf"         # output filename for main results (time vs. acf)
max_lag = 100               # compute acf up to t = max_lag*dt
nskiptpt = 5000             # discard this many initial timepoints when computing acf

###################
# before we start #
###################

# read simulation parameters from the JSON file
with open(os.path.join(logdir,'sim_params.txt')) as f:
    var_data = json.load(f)

Nrun = var_data["Nrun"]
Nstep = var_data["Nstep"]
ra1 = var_data["ra1"]
rd1 = var_data["rd1"]
ra2 = var_data["ra2"]
rd2 = var_data["rd2"]
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

# read surfcov / compute and store acf and ccf
all_ccf_1_1 = np.zeros((Nrun,max_lag+1))
all_ccf_2_1 = np.zeros((Nrun,max_lag+1))
all_ccf_1_2 = np.zeros((Nrun,max_lag+1))
all_ccf_2_2 = np.zeros((Nrun,max_lag+1))

for i, surfcov_file in enumerate(surfcov_files):
    data = np.loadtxt(surfcov_file)
    surfcov1 = data[nskiptpt:,1]
    surfcov2 = data[nskiptpt:,2]
    all_ccf_1_1[i] = compute_ccf(surfcov1, surfcov1, max_lag) # ACF of surfcov1
    all_ccf_2_1[i] = compute_ccf(surfcov2, surfcov1, max_lag) # CCF of surfcov2 and surfcov1
    all_ccf_1_2[i] = compute_ccf(surfcov1, surfcov2, max_lag) # CCF of surfcov1 and surfcov2
    all_ccf_2_2[i] = compute_ccf(surfcov2, surfcov2, max_lag)  # ACF of surfcov2

#############################################
# computee the average acf and standard err #
#############################################

mean_ccf_1_1 = np.mean(all_ccf_1_1,axis=0)
var_ccf_1_1 = np.var(all_ccf_1_1,ddof=1,axis=0)
stderr_ccf_1_1 = np.sqrt(var_ccf_1_1/Nrun)

mean_ccf_2_1 = np.mean(all_ccf_2_1,axis=0)
var_ccf_2_1 = np.var(all_ccf_2_1,ddof=1,axis=0)
stderr_ccf_2_1 = np.sqrt(var_ccf_2_1/Nrun)

mean_ccf_1_2 = np.mean(all_ccf_1_2,axis=0)
var_ccf_1_2 = np.var(all_ccf_1_2,ddof=1,axis=0)
stderr_ccf_1_2 = np.sqrt(var_ccf_1_2/Nrun)

mean_ccf_2_2 = np.mean(all_ccf_2_2,axis=0)
var_ccf_2_2 = np.var(all_ccf_2_2,ddof=1,axis=0)
stderr_ccf_2_2 = np.sqrt(var_ccf_2_2/Nrun)

###########################
# compute theoretical acf #
###########################

tpts = dt*np.arange(max_lag+1)
theo_acf = np.zeros(max_lag+1)
# Not used 
#for i in range(max_lag+1):
#    theo_acf[i] = theory_acf_1site_ads(tpts[i],ra1,rd1,nsite)

####################
# data file output #
####################

fullpath_outfile=os.path.join(resdir,outfile)
np.savetxt(fullpath_outfile,np.column_stack([tpts,
                                            mean_ccf_1_1, stderr_ccf_1_1,
                                            mean_ccf_2_1, stderr_ccf_2_1,
                                            mean_ccf_1_2, stderr_ccf_1_2,
                                            mean_ccf_2_2, stderr_ccf_2_2]),
            header="time\tccf_1_1\tstd_err11\tccf_2_1\tstd_err21\tccf_1_2\tstd_err12\tccf_2_2\tstd_err22")
print("\ndata file saved as %s" % fullpath_outfile)
