import matplotlib.pyplot as plt
import numpy as np
import os

def plot_single_coverage(data_file):
    # Check if file exists
    if not os.path.exists(data_file):
        print("Data file not found: {0}".format(data_file))
        return
        
    # Load data
    data = np.loadtxt(data_file)
    time = data[:, 0]
    coverage = data[:, 1]
    
    # Convert coverage to ratio
    coverage_ratio = coverage / np.max(coverage)
    
    # Create figure
    plt.figure(figsize=(10, 6))
    
    # Plot coverage ratio
    plt.plot(time, coverage_ratio, 'b-', linewidth=2, label='Coverage Ratio')
    
    # Customize the plot
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Coverage Ratio', fontsize=12)
    plt.title('Surface Coverage Over Time - Single Trajectory', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the plot
    output_path = os.path.join(os.path.dirname(data_file), 'single_coverage_plot.png')
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print("Plot saved as: {0}".format(output_path))
    plt.show()
    
# Call the function with a single data file
plot_single_coverage('../res_1000/data1.txt')
