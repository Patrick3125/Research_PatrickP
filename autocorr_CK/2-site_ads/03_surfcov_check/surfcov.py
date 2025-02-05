import matplotlib.pyplot as plt
import numpy as np
import math
import os
import sys
import json
import glob

def theory_steady_state_surfcov_2site_ads(ra,rd,nsite):
    mean = 1/(1+math.sqrt(rd/ra))
    variance = mean*(1-mean)/nsite
    return [mean,variance]

#########################
# changeable parameters #
#########################

logdir = "../log"           # directory of sim_params.txt (input)
resdir = "../res"           # directory of surfcov files (input) and output files

outfile = "res.surfcov_avg" # output filename for main results (time vs. average surfcov)

nskiptpt = 1000             # number of initial time points to be skipped when calculating steady-state stats

gen_plot = True             # whether a figure is generated     
figfile = "surfcov.png"     # figure filename 
nerrbar  = 50

nindcurve = 1               # how many individual run curves to be included (0 or pos int) 
ind_color = 'lightblue'     # plot parameters for individual curves: line color
ind_alpha = 1.0             # opacity
ind_lw = 0.5                # line width

###################
# before we start #
###################

# read simulation parameters from the JSON file
with open(os.path.join(logdir,'sim_params.txt')) as f:
    var_data = json.load(f)

Nrun = var_data["Nrun"]
Nstep = var_data["Nstep"]
ra2 = var_data["ra2"]
rd2 = var_data["rd2"]
xhi = var_data["xhi"] 
yhi = var_data["yhi"]

# compute needed variables
nsite = xhi*yhi
ra = 2*ra2
rd = 2*rd2

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
timepoints = first_data[:,0]
if not Nstep==len(timepoints): 
    print("Nstep=%d but there are %d time points in %s" % (Nstep,len(timepoints),surfcov_files[0])) 
    sys.exit(0) 

# read and save
all_surfcov = np.zeros((Nrun,Nstep))
for i, surfcov_file in enumerate(surfcov_files):
    data = np.loadtxt(surfcov_file)
    surfcov = data[:,1]
    all_surfcov[i] = surfcov 

#################################################
# computee the average surfcov and standard err #
#################################################

mean_surfcov = np.mean(all_surfcov,axis=0)
var_surfcov = np.var(all_surfcov,ddof=1,axis=0)
stderr_surfcov = np.sqrt(var_surfcov/Nrun)

####################
# data file output #
####################

fullpath_outfile=os.path.join(resdir,outfile)
np.savetxt(fullpath_outfile,np.column_stack([timepoints,mean_surfcov,stderr_surfcov]),header="time\tsurfcov\tstderr")
print("\ndata file saved as %s" % fullpath_outfile)

#######################################################################
# compare the steady-state mean and variance with theoretical results #
#######################################################################

# theoretical results
[theo_mean_ss_surfcov,theo_var_ss_surfcov] = theory_steady_state_surfcov_2site_ads(ra,rd,nsite)

# simulation results
mean_surfcov_per_run = np.zeros(Nrun)
var_surfcov_per_run = np.zeros(Nrun)

for i in range(Nrun):
    mean_surfcov_per_run[i] = np.mean(all_surfcov[i,nskiptpt:Nstep])
    var_surfcov_per_run[i] = np.var(all_surfcov[i,nskiptpt:Nstep],ddof=1)

mean1 = np.mean(mean_surfcov_per_run)
std1 = math.sqrt(np.var(mean_surfcov_per_run,ddof=1)/Nrun)
mean2 = np.mean(var_surfcov_per_run)
std2 = math.sqrt(np.var(var_surfcov_per_run,ddof=1)/Nrun)

# screen output
print("\nComparing theoretical and simulation results (nskiptpt=%f, Nrun=%d)" % (nskiptpt,Nrun))
print("1. Mean steady-state surface coverage:")
print("   Theory:     %e" % theo_mean_ss_surfcov)
print("   Simulation: %e (std err=%e)" % (mean1,std1))

print("\n2. Variance of steady-state surface coverage:")
print("   Theory:     %e" % theo_var_ss_surfcov)
print("   Simulation: %e (std err=%e)" % (mean2,std2))

#################
# figure output #
#################

if gen_plot:

    # create figure with a reasonable size
    plt.figure(figsize=(12,8))

    # draw the average surfcov
    plt.plot(timepoints,mean_surfcov,'r-',linewidth=1,label='Average over %d Runs'%Nrun)

    # draw error bars
    freq = Nstep/nerrbar
    plt.errorbar(timepoints[0:Nstep:freq], mean_surfcov[0:Nstep:freq],2*stderr_surfcov[0:Nstep:freq],linewidth=0,elinewidth=1,capsize=2,ecolor='k')

    # add individual run curves
    for i in range(nindcurve):
         plt.plot(timepoints,all_surfcov[i],ind_color,alpha=ind_alpha,linewidth=ind_lw)

    # create an item in the legend if individual curves are drawn  
    if nindcurve==1:
        plt.plot([],[],ind_color,alpha=ind_alpha,label='Individual Run',linewidth=ind_lw)
    elif nindcurves>1:
        plt.plot([],[],ind_color,alpha=ind_alpha,label='Individual Runs',linewidth=ind_lw)

    # customize the plot
    plt.xlabel('Time',fontsize=12)
    plt.ylabel('Surface Coverage',fontsize=12)
    plt.grid(True,alpha=0.3)
    plt.legend(fontsize=10)

    # save and show the plot
    fullpath_figfile=os.path.join(resdir,figfile)
    plt.savefig(fullpath_figfile,dpi=300,bbox_inches='tight')
    print("\nfigure file saved as %s" % fullpath_figfile)

    plt.tight_layout()
    plt.show()
