import matplotlib.pyplot as plt
import numpy as np
import os

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
        ax.plot(tau_values, individual_corrs, '-', color='lightblue', alpha=0.2, linewidth=1, zorder=1)
    except IOError:
        print("corr{}.txt not found. Skipping...".format(i))
ax.plot(1, 1, '-', color='lightblue', alpha=0.2, linewidth=1, label="individual correlation", zorder=1)
# Plot the average correlations
ax.plot(tau_values, average_corrs, '-', color='blue', linewidth=2, label="Average Correlation", zorder=2)
# Plot the error bars at an interval using standard error
errbar_interval = 3  # Show error bars every 3 points
ax.errorbar(tau_values[::errbar_interval],
           average_corrs[::errbar_interval],
           yerr=standard_error[::errbar_interval],
           fmt='', ecolor='red', zorder=3)
# Calculate tangent lines at t=0 and t=100
def get_tangent_line(t_point):
    # Find the nearest index to the desired t point
    idx = np.argmin(np.abs(tau_values - t_point))

    # For t=0, use the first two points to calculate forward difference
    if t_point == 0:
        dt = tau_values[100] - tau_values[0]
        d_log_y = np.log(average_corrs[100]) - np.log(average_corrs[0])
        slope = d_log_y / dt
        y_point = average_corrs[0]
        x_ref = tau_values[0]
    # For other points, use central difference if possible
    elif idx > 0 and idx < len(tau_values) - 1:
        dt = tau_values[idx + 1] - tau_values[idx - 1]
        d_log_y = np.log(average_corrs[idx + 1]) - np.log(average_corrs[idx - 1])
        slope = d_log_y / dt
        y_point = average_corrs[idx]
        x_ref = tau_values[idx]
    else:
        return None, None, None, None

    # Create the tangent line in log space
    x_line = np.array([tau_values[0], tau_values[-1]])
    log_y_line = np.log(y_point) + slope * (x_line - x_ref)
    y_line = np.exp(log_y_line)

    return x_line, y_line, "Tangent at t={:.2f} (slope={:.15f})".format(t_point, slope), slope
# Add tangent lines
styles = ['--', '-.']
colors = ['g', 'g']
t_points = [0, 1000]
# Store slopes for possible analysis
slopes = []
for t_point, style, color in zip(t_points, styles, colors):
    x_line, y_line, label, slope = get_tangent_line(t_point)
    if x_line is not None:
        ax.plot(x_line, y_line, style, color=color, alpha=0.7,
                label=label, linewidth=1.5, zorder=4)  # Higher zorder to be on top
        slopes.append(slope)
# Set scale and labels
plt.yscale('log')
ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('')
ax.grid(False)
ax.legend(loc='upper right')
# zoom into average
ax.set_xlim([np.min(tau_values), np.max(tau_values)])
ax.set_ylim([np.min(average_corrs) * 0.99, np.max(average_corrs) * 1.01])
plt.savefig('semilog_plot', dpi=300, bbox_inches='tight')
plt.show()
# Print slopes for reference
print("\nCalculated slopes:")
for t_point, slope in zip(t_points, slopes):
    print("At t={}: {:.15f}".format(t_point, slope))
