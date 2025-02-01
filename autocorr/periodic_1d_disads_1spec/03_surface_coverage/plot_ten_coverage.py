import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import random

def plot_coverage_data(res_dir):
    # Create figure with reasonable size
    plt.figure(figsize=(12, 8))
    
    # Get list of all data files and sort them
    data_files = sorted(glob.glob(os.path.join(res_dir, 'data*.txt')))
    if not data_files:
        print("No data files found in directory:", res_dir)
        return
        
    # Randomly sample 10 files if there are more than 10 files
    n_files = min(1000, len(data_files))
    if len(data_files) > 1000:
        data_files = random.sample(data_files, n_files)
        data_files.sort()  # Sort the sampled files for consistency
    
    print("Plotting {} data files".format(n_files))
    
    # Initialize array to store all coverage ratios
    first_data = np.loadtxt(data_files[0])
    time = first_data[:, 0]
    n_timepoints = len(time)
    all_coverage_ratios = np.zeros((n_files, n_timepoints))
    
    # Plot individual data files and store ratios
    for i, data_file in enumerate(data_files):
        data = np.loadtxt(data_file)
        coverage = data[:, 1]
        # Convert coverage to ratio
        coverage_ratio = coverage / np.max(coverage)
        all_coverage_ratios[i] = coverage_ratio
        plt.plot(time, coverage_ratio, 'lightblue', alpha=0.3, linewidth=1)  # Increased alpha and linewidth for better visibility
    
    # Add one light blue line to legend for individual runs
    plt.plot([], [], 'lightblue', alpha=0.5, label='Individual Runs', linewidth=1)
    
    # Calculate and plot the mean coverage ratio
    mean_coverage = np.mean(all_coverage_ratios, axis=0)
    plt.plot(time, mean_coverage, 'r-', linewidth=2, label='Average Coverage')
    
    # Customize the plot
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Coverage Ratio', fontsize=12)
    plt.title('Surface Coverage Over Time - {} Runs with Average'.format(n_files), fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    
    # Save the plot
    plt.savefig(os.path.join(res_dir, 'coverage_plot.png'), dpi=300, bbox_inches='tight')
    print("Plot saved as: {0}".format(os.path.join(res_dir, 'coverage_plot.png')))
    plt.show()
    
# Call the function with the specified directory
plot_coverage_data('../res_1000')
