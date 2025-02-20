import numpy as np
import os
import sys
import json
import glob

logdir = "../log"           # directory of sim_params.txt
resdir = "../res"           # directory of surfcov files
trajdir = "../traj"         # directory of traj files (output)

########
# argv #
########

if len(sys.argv) != 4:
    print("Usage: python %s <num_of_traj_files> <num_of_time_points> <freq>" % sys.argv[0])
    sys.exit(0)

ntraj = int(sys.argv[1])
ntpt = int(sys.argv[2])
freq = int(sys.argv[3])

##############
# sim params # 
##############

with open(os.path.join(logdir,'sim_params.txt')) as f:
    var_data = json.load(f)

Nrun = var_data["Nrun"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]

#########
# check #
#########

if Nrun<ntraj:
    print("ERROR: Nrun=%d < ntraj=%d" % (Nrun,ntraj))
    sys.exit(0)

if Nstep < (ntpt-1)*freq+1:
    print("ERROR: Nstep=%d < (ntpt-1)*freq+1=%d" % (Nstep,(ntpt-1)*freq+1))
    sys.exit(0)

print("Nrun=%d" % Nrun)
print("ntraj=%d" % ntraj)
print("\nNstep=%d" % Nstep)
print("ntpt=%d, freq=%d, (ntpt-1)*freq+1=%d" % (ntpt,freq,(ntpt-1)*freq+1))
print("deltat=%e" % deltat)
print("freq*deltat=%e" % (freq*deltat))

################
# double check #
################

# get the list of all surfcov files and sort them
surfcov_files = sorted(glob.glob(os.path.join(resdir,'surfcov*.txt')))
if not surfcov_files:
    print("no surfcov files found in %s" % resdir)
    os.exit(0) 
print("\n%d surfcov files found in %s" % (len(surfcov_files),resdir))

# check the number of surfcov files
if Nrun!=len(surfcov_files):
    print("Nrun=%d but there are %d surfcov files in %s" % (Nrun,len(surfcov_files),resdir))
    sys.exit(0) 

# check the number of time points in each file
first_data = np.loadtxt(surfcov_files[0])
timepoints = first_data[:,0]
if Nstep!=len(timepoints): 
    print("Nstep=%d but there are %d time points in %s" % (Nstep,len(timepoints),surfcov_files[0])) 
    sys.exit(0) 

#################
# read and save #
################

for i in range(ntraj):
    filename1 = resdir+'/surfcov{0}.txt'.format(i+1)
    filename2 = trajdir+'/traj{0}.txt'.format(i+1)
    print("%s -> %s" % (filename1,filename2))

    [surfcov1,surfcov2] = np.loadtxt(filename1,usecols=(1,2),unpack=True)

    start=Nstep-(ntpt-1)*freq-1
    np.savetxt(filename2,np.column_stack([surfcov1[start:Nstep:freq],surfcov2[start:Nstep:freq]]))

