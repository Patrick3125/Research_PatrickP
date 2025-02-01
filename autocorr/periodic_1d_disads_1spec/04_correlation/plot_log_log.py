import matplotlib.pyplot as plt
import numpy as np
import os

# Path whre the files are stored
logdir = "../" + sorted(d for d in os.listdir("..") if d.startswith("log_"))[-1]
resdir = "../" + sorted(d for d in os.listdir("..") if d.startswith("res_"))[-1]


# Read the number of runs from the header
with open(os.path.join(resdir, "average_corr.txt"), 'r') as f:
    header1 = f.readline()
    header2 = f.readline()
    Nruns = int(header1.split('=')[1].split('\n')[0].strip())
    deltat = float(header2.split('=')[1].split('\n')[0].strip())

# Detect the number of correlation data files
correlation_files = [f for f in os.listdir(resdir) if f.startswith('corr')]
num_files = len(correlation_files)

# Read the saved average correlation data
data = np.loadtxt(os.path.join(resdir, "average_corr.txt"))
tau_values = data[:, 0] * 0.01
average_corrs = data[:, 1]
variances = data[:, 2]

# Calculate standard error
standard_error = np.sqrt(variances / Nruns)

fig, ax = plt.subplots()

# Plot each individual correlation data
for i in range(1, num_files + 1):
    try:
        individual_data = np.loadtxt(os.path.join(resdir, "corr{}.txt".format(i)))
        individual_corrs = individual_data[:, 1]
        # Add small epsilon to avoid log(0)
        epsilon = 1e-10
        ax.plot(tau_values + epsilon, individual_corrs + epsilon, '-', 
                color='lightblue', alpha=0.2, linewidth=1, zorder=1)
    except IOError:
        print("corr{}.txt not found. Skipping...".format(i))

ax.plot(1, 1, '-', color='lightblue', alpha=0.2, linewidth=1, 
        label="individual correlation", zorder=1)

# Plot the average correlations
ax.plot(tau_values + epsilon, average_corrs + epsilon, '-', 
        color='blue', linewidth=2, label="Average Correlation", zorder=2)

# Plot the error bars at an interval using standard error
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(tau_values[::errbar_interval] + epsilon,
           average_corrs[::errbar_interval] + epsilon,
           yerr=standard_error[::errbar_interval],
           fmt='none', ecolor='red', zorder=3)

# Calculate tangent lines at t=0 and t=100
def get_tangent_line(t_point):
    # Find the nearest index to the desired t point
    idx = np.argmin(np.abs(tau_values - t_point))
    
    # For t=0, use the first two points to calculate forward difference
    if t_point == 0:
        dt = np.log(tau_values[1] + epsilon) - np.log(tau_values[0] + epsilon)
        d_log_y = np.log(average_corrs[1] + epsilon) - np.log(average_corrs[0] + epsilon)
        slope = d_log_y / dt
        y_point = average_corrs[0]
        x_ref = tau_values[0]
    # For other points, use central difference if possible
    elif idx > 0 and idx < len(tau_values) - 1:
        dt = np.log(tau_values[idx + 1] + epsilon) - np.log(tau_values[idx - 1] + epsilon)
        d_log_y = np.log(average_corrs[idx + 1] + epsilon) - np.log(average_corrs[idx - 1] + epsilon)
        slope = d_log_y / dt
        y_point = average_corrs[idx]
        x_ref = tau_values[idx]
    else:
        return None, None, None, None

    # Create the tangent line in log-log space
    x_line = np.array([tau_values[0], tau_values[-1]])
    log_y_line = np.log(y_point + epsilon) + slope * (np.log(x_line + epsilon) - np.log(x_ref + epsilon))
    y_line = np.exp(log_y_line) - epsilon

    return x_line, y_line, "Tangent at t={:.2f} (slope={:.15f})".format(t_point, slope), slope


# Add reference slopes (-1 and -0.5)
def add_reference_slope(slope, x_range, label):
    # Get the y values at the midpoint of the average correlation data
    mid_idx = len(average_corrs) // 2
    y_mid = average_corrs[mid_idx]
    x_mid = tau_values[mid_idx]
    
    # Create the line with the desired slope in log space
    x_line = np.array(x_range)
    log_y_line = np.log(y_mid + epsilon) + slope * (np.log(x_line + epsilon) - np.log(x_mid + epsilon))
    y_line = np.exp(log_y_line) - epsilon
    
    return x_line, y_line

# Add reference slopes before the tangent lines
x_range = [np.min(tau_values), np.max(tau_values)]

# Add slope -1
x_line_1, y_line_1 = add_reference_slope(-1, x_range, "Slope -1")
ax.plot(x_line_1 + epsilon, y_line_1 + epsilon, '--', color='red', alpha=0.7,
        label="Slope -1", linewidth=1.5, zorder=5)

# Add slope -0.5
x_line_05, y_line_05 = add_reference_slope(-0.5, x_range, "Slope -0.5")
ax.plot(x_line_05 + epsilon, y_line_05 + epsilon, '--', color='orange', alpha=0.7,
        label="Slope -0.5", linewidth=1.5, zorder=5)

# Add slope -0.5
x_line_05, y_line_05 = add_reference_slope(-1.5, x_range, "Slope -0.5")
ax.plot(x_line_05 + epsilon, y_line_05 + epsilon, '--', color='green', alpha=0.7,
        label="Slope -1.5", linewidth=1.5, zorder=5)

# Plot the average correlations
ax.plot(tau_values + epsilon, average_corrs + epsilon, '-', 
        color='blue', linewidth=2, label="Average Correlation", zorder=2)

# Plot the error bars at an interval using standard error
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(tau_values[::errbar_interval] + epsilon,
           average_corrs[::errbar_interval] + epsilon,
           yerr=standard_error[::errbar_interval],
           fmt='none', ecolor='red', zorder=3)

# Add tangent lines
styles = ['--', '-.']
colors = ['g', 'g']
t_points = [0, 300]
# Store slopes for possible analysis
slopes = []

for t_point, style, color in zip(t_points, styles, colors):
    x_line, y_line, label, slope = get_tangent_line(t_point)
    if x_line is not None:
#        ax.plot(x_line + epsilon, y_line + epsilon, style, color=color, alpha=0.7,
#                label=label, linewidth=1.5, zorder=4)
        slopes.append(slope)

# Set both axes to logarithmic scale
plt.xscale('log')
plt.yscale('log')

ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('Log-Log Plot of Correlation Data')
ax.grid(True, which="both", ls="-", alpha=0.2)
ax.legend(loc='upper right')

# Adjust limits to avoid zeros
ax.set_xlim([np.min(tau_values + epsilon), np.max(tau_values)])
ax.set_ylim([np.min(average_corrs + epsilon), np.max(average_corrs)])

plt.savefig('loglog_plot', dpi=300, bbox_inches='tight')
plt.show()

# Print slopes for reference
print("\nCalculated slopes (in log-log space):")
for t_point, slope in zip(t_points, slopes):
    print("At t={}: {:.15f}".format(t_point, slope))
