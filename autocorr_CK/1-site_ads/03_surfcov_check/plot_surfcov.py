import matplotlib.pyplot as plt
import numpy as np
import os
import glob

def plot_surfcov(res_dir,total_sites,nindcurves):
    
    ind_color = 'lightblue'
    ind_alpha = 1.0
    ind_lw = 0.5
    nerrbars = 50
    figfilename = "surfcov.png"

    # Create figure with reasonable size
    plt.figure(figsize=(12, 8))
    
    # Get list of all surfcov files and sort them
    surfcov_files = sorted(glob.glob(os.path.join(res_dir, 'surfcov*.txt')))
    if not surfcov_files:
        print("No surfcov files found in directory:", res_dir)
        return
        
    print("Found {0} surfcov files".format(len(surfcov_files)))
    
    # Initialize array to store all coverage ratios
    first_data = np.loadtxt(surfcov_files[0])
    time = first_data[:, 0]
    n_timepoints = len(time)
    all_surfcov = np.zeros((len(surfcov_files), n_timepoints))
    
    # Plot individual data files and store ratios
    for i, surfcov_file in enumerate(surfcov_files):
        data = np.loadtxt(surfcov_file)
        surfcov = data[:, 1]
        all_surfcov[i] = surfcov 
        # Include the first nindcurves curves to the plot
        if i<nindcurves:
            plt.plot(time, surfcov, ind_color, alpha=ind_alpha, linewidth=ind_lw)
    
    # Add one light blue line to legend for individual runs
    if nindcurves==1:
        plt.plot([], [], ind_color, alpha=ind_alpha, label='Individual Run', linewidth=ind_lw)
    elif nindcurves>1:
        plt.plot([], [], ind_color, alpha=ind_alpha, label='Individual Runs', linewidth=ind_lw)
    
    # Calculate and plot the mean
    mean_surfcov = np.mean(all_surfcov, axis=0)
    plt.plot(time, mean_surfcov, 'r-', linewidth=1, label='Mean')
    
    # Calculate the std err and plot error bars
    var_surfcov = np.var(all_surfcov, ddof=1, axis=0)
    stderr = np.sqrt(var_surfcov/len(surfcov_files))
    freq = n_timepoints/nerrbars
    plt.errorbar(time[0:n_timepoints:freq], mean_surfcov[0:n_timepoints:freq], 2*stderr[0:n_timepoints:freq],linewidth=0,elinewidth=1,capsize=2,ecolor='k')
    
    # Customize the plot
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Surface Coverage', fontsize=12)
    plt.title('Surface Coverage - Averaged over {0} Runs'.format(len(surfcov_files)), fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(res_dir, figfilename), dpi=300, bbox_inches='tight')
    print("Plot saved as: {0}".format(os.path.join(res_dir, figfilename)))
    plt.show()
