import matplotlib.pyplot as plt
import numpy as np
import math
import os
import sys
import json
import glob

def theory_steady_state_surfcov_1site_ads(ra1,rd1,ra2,rd2,nsite):
    mean1 = ra1*rd2/(ra1*rd2+rd1*ra2+rd1*rd2)
    mean2 = rd1*ra2/(ra1*rd2+rd1*ra2+rd1*rd2)
    variance1 = mean1*(1-mean1)/nsite
    variance2 = mean2*(1-mean2)/nsite
    return [mean1,mean2,variance1,variance2]

#########################
# changeable parameters #
#########################

logdir = "../log"           # directory of sim_params.txt (input)
resdir = "../res"           # directory of surfcov files (input) and output files

outfile = "res.surfcov_avg" # output filename for main results (time vs. average surfcov)

nskiptpt = 10000            # number of initial time points to be skipped when calculating steady-state stats

gen_plot = True             # whether a figure is generated     
figfile = "surfcov.png"     # figure filename 
nerrbar  = 50

nindcurve = 1               # how many individual run curves to be included (0 or pos int) 
ind_color1 = 'lightblue'    # plot parameters for individual curves (spec1): line color
ind_color2 = 'lightblue'   # plot parameters for individual curves (spec2): line color
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
ra1 = var_data["ra1"]
rd1 = var_data["rd1"]
ra2 = var_data["ra2"]
rd2 = var_data["rd2"]
xhi = var_data["xhi"] 
yhi = var_data["yhi"]

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
timepoints = first_data[:,0]
if not Nstep==len(timepoints): 
    print("Nstep=%d but there are %d time points in %s" % (Nstep,len(timepoints),surfcov_files[0])) 
    sys.exit(0) 

# read and save
all_surfcov1 = np.zeros((Nrun,Nstep))
all_surfcov2 = np.zeros((Nrun,Nstep))
for i, surfcov_file in enumerate(surfcov_files):
    data = np.loadtxt(surfcov_file)
    surfcov1 = data[:,1]
    all_surfcov1[i] = surfcov1
    surfcov2 = data[:,2]
    all_surfcov2[i] = surfcov2

#################################################
# computee the average surfcov and standard err #
#################################################

mean_surfcov1 = np.mean(all_surfcov1,axis=0)
mean_surfcov2 = np.mean(all_surfcov2,axis=0)
var_surfcov1 = np.var(all_surfcov1,ddof=1,axis=0)
var_surfcov2 = np.var(all_surfcov2,ddof=1,axis=0)
stderr_surfcov1 = np.sqrt(var_surfcov1/Nrun)
stderr_surfcov2 = np.sqrt(var_surfcov2/Nrun)

####################
# data file output #
####################

fullpath_outfile=os.path.join(resdir,outfile)
np.savetxt(fullpath_outfile,np.column_stack([timepoints,mean_surfcov1,stderr_surfcov1,mean_surfcov2,stderr_surfcov2]),header="time\tsurfcov1\tstderr1\tsurfcov2\tstderr2")
print("\ndata file saved as %s" % fullpath_outfile)

#######################################################################
# compare the steady-state mean and variance with theoretical results #
#######################################################################

# theoretical results
[theo_mean_ss_surfcov1,theo_mean_ss_surfcov2,theo_var_ss_surfcov1,theo_var_ss_surfcov2] = theory_steady_state_surfcov_1site_ads(ra1,rd1,ra2,rd2,nsite)

# simulation results
mean1_surfcov_per_run = np.zeros(Nrun)
mean2_surfcov_per_run = np.zeros(Nrun)
var1_surfcov_per_run = np.zeros(Nrun)
var2_surfcov_per_run = np.zeros(Nrun)

for i in range(Nrun):
    mean1_surfcov_per_run[i] = np.mean(all_surfcov1[i,nskiptpt:Nstep])
    var1_surfcov_per_run[i] = np.var(all_surfcov1[i,nskiptpt:Nstep],ddof=1)
    mean2_surfcov_per_run[i] = np.mean(all_surfcov2[i,nskiptpt:Nstep])
    var2_surfcov_per_run[i] = np.var(all_surfcov2[i,nskiptpt:Nstep],ddof=1)

mean_mean1 = np.mean(mean1_surfcov_per_run)
std_mean1 = math.sqrt(np.var(mean1_surfcov_per_run,ddof=1)/Nrun)
mean_mean2 = np.mean(mean2_surfcov_per_run)
std_mean2 = math.sqrt(np.var(mean2_surfcov_per_run,ddof=1)/Nrun)
mean_var1 = np.mean(var1_surfcov_per_run)
std_var1 = math.sqrt(np.var(var1_surfcov_per_run,ddof=1)/Nrun)
mean_var2 = np.mean(var2_surfcov_per_run)
std_var2 = math.sqrt(np.var(var2_surfcov_per_run,ddof=1)/Nrun)

# screen output
print("\nComparing theoretical and simulation results (nskiptpt=%d, Nrun=%d)" % (nskiptpt,Nrun))
print("1. Mean steady-state surface coverage:")
print("   Theory:     %e" % theo_mean_ss_surfcov1)
print("   Simulation: %e (std err=%e)" % (mean_mean1,std_mean1))
print("   Theory:     %e" % theo_mean_ss_surfcov2)
print("   Simulation: %e (std err=%e)" % (mean_mean2,std_mean2))

print("\n2. Variance of steady-state surface coverage:")
print("   Theory:     %e" % theo_var_ss_surfcov1)
print("   Simulation: %e (std err=%e)" % (mean_var1,std_var1))
print("   Theory:     %e" % theo_var_ss_surfcov2)
print("   Simulation: %e (std err=%e)" % (mean_var2,std_var2))

#################
# figure output #
#################

if gen_plot:

    # create figure with a reasonable size
    plt.figure(figsize=(12,8))

    # draw the average surfcov
    plt.plot(timepoints,mean_surfcov1,'r-',linewidth=1,label='spec1 (average over %d Runs)'%Nrun)
    plt.plot(timepoints,mean_surfcov2,'g-',linewidth=1,label='spec2 (average over %d Runs)'%Nrun)

    # draw error bars
    freq = Nstep/nerrbar
    plt.errorbar(timepoints[0:Nstep:freq],mean_surfcov1[0:Nstep:freq],2*stderr_surfcov1[0:Nstep:freq],linewidth=0,elinewidth=1,capsize=2,ecolor='k')
    plt.errorbar(timepoints[0:Nstep:freq],mean_surfcov2[0:Nstep:freq],2*stderr_surfcov2[0:Nstep:freq],linewidth=0,elinewidth=1,capsize=2,ecolor='k')

    # add individual run curves
    for i in range(nindcurve):
         plt.plot(timepoints,all_surfcov1[i],ind_color1,alpha=ind_alpha,linewidth=ind_lw)
         plt.plot(timepoints,all_surfcov2[i],ind_color2,alpha=ind_alpha,linewidth=ind_lw)

    # create an item in the legend if individual curves are drawn  
    if nindcurve==1:
        plt.plot([],[],ind_color1,alpha=ind_alpha,label='Individual Run (spec1)',linewidth=ind_lw)
        plt.plot([],[],ind_color2,alpha=ind_alpha,label='Individual Run (spec2)',linewidth=ind_lw)
    elif nindcurves>1:
        plt.plot([],[],ind_color1,alpha=ind_alpha,label='Individual Runs (spec1)',linewidth=ind_lw)
        plt.plot([],[],ind_color2,alpha=ind_alpha,label='Individual Runs (spec2)',linewidth=ind_lw)

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
