import matplotlib.pyplot as plt
import numpy as np
import math
import sys
import os

# Automatically detect the number of log files
log_files = [f for f in os.listdir('.') if f.startswith('log') and f.endswith('.spparks')]
num_files = len(log_files)
print(num_files)
#num_files = 16
maxtau = 250
size = 90000
errbar_interval = 3  # Show error bars every point

all_corrs = []
average_corrs = np.zeros(maxtau - 1)
variances = np.zeros(maxtau - 1)

# Loop through all log files
for i in range(0, num_files-1):
    #print(gf)
    x_values = []
    y_values = []

    filename = "log{}.spparks".format(i)

    rd = float(sys.argv[1])
    ra = float(sys.argv[2])
    theta = 1 / (1 + math.sqrt(rd / ra))

    with open(filename, "r") as f:
        lines = f.readlines()[81:]

        start_from = True
        for line in lines:
            if "- nreaction = 0" in line:
                start_from = True
                continue
            if start_from and line.split()[0] == "Loop":
                start_from = False
                continue
            if start_from:
     #           print(line, i)
                x_values.append(float(line.split()[0]) / size)
                y_values.append(float(line.split()[6]) / size)

    corrs = []
    new_values = np.array(y_values)
    new_values -= theta
    for tau in range(1, maxtau):
        new_x = new_values[:-tau]
        new_y = new_values[tau:]
        corrs.append(np.corrcoef(new_x, new_y)[0, 1])

    all_corrs.append(corrs)
    average_corrs += np.array(corrs)

average_corrs /= num_files

# Calculate the variance for each point
for tau in range(maxtau - 1):
    mean_value = average_corrs[tau]
    variance = sum((np.array([corrs[tau] for corrs in all_corrs]) - mean_value)**2) / (num_files - 1)
    variances[tau] = variance

fig, ax = plt.subplots()

#ax.errorbar(range(1, maxtau)[::errbar_interval],
#            average_corrs[::errbar_interval],
#            yerr=np.sqrt(variances[::errbar_interval]),
            #yerr=np.sqrt(variances[::errbar_interval]),
#            fmt='', ecolor='green')


# Plot just the error bars at interval
ax.errorbar(range(1, maxtau)[::errbar_interval], 
            average_corrs[::errbar_interval],
            #yerr=2*np.sqrt(variances[::errbar_interval]/(num_files-1)),
            yerr=np.sqrt(variances[::errbar_interval]), 
            fmt='', ecolor='red')



for i, corrs in enumerate(all_corrs):
    ax.plot(range(1, maxtau), corrs, '-', color='lightblue', alpha=0.2, linewidth=1,zorder=-32)

#ax.set_xscale('log', basex=10)
#ax.set_yscale('log', basey=10)

ax.set_xlabel('tau')
ax.set_ylabel('correlation')
ax.set_title('Graphs from log files')
ax.grid(True)
ax.legend(['Sims'], loc='upper right')

plt.show()


