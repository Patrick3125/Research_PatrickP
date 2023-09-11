import numpy as np
import math
import sys
import os

# Automatically detect the number of log files
log_folder = "../01_run_diss_ads/"
#log_folder = "../"
log_files = [f for f in os.listdir(log_folder) if f.startswith('log') and f.endswith('.spparks')]
num_files = len(log_files)
print(num_files)
num_files = 60
maxtau = 250
#size will be read from file.
size = 1

all_corrs = []
average_corrs = np.zeros(maxtau - 1)
variances = np.zeros(maxtau - 1)


# Loop through all log files
for i in range(1, num_files+1):
    x_values = []
    y_values = []
    filename = os.path.join(log_folder, "log{}.spparks".format(i))
    rd = float(sys.argv[1])
    ra = float(sys.argv[2])
    theta = 1 / (1 + math.sqrt(rd / ra))

    with open(filename, "r") as f:
        lines = f.readlines()[79:]

        start_from = False
        last_line_before_loop = None

        for line in lines:
            if "- nreaction = 0" in line or  "Naccept" in line:
                start_from = True
                continue
            if start_from and line.split()[0] == "Loop":
                start_from = False
                if last_line_before_loop is not None:
                    x_values.append(float(last_line_before_loop.split()[0]))
                    y_values.append(float(last_line_before_loop.split()[6]) / size)
                continue
            if start_from:
                last_line_before_loop = line
                if float(line.split()[0]) == 0:
                    x_values.append(float(line.split()[0]))
                    size = float(line.split()[5])
                    y_values.append(float(line.split()[6]) / size)


    corrs = []
    new_values = np.array(y_values)
    new_values -= theta

    for tau in range(1, maxtau):
        new_x = new_values[:-tau]
        new_y = new_values[tau:]
        corrs.append(np.corrcoef(new_x, new_y)[0, 1])

    individual_data_to_save = np.column_stack((range(1, maxtau), corrs))
    np.savetxt(f"correlation_data_log{i}.txt", individual_data_to_save, fmt="%d %f", header="i correlation")
    all_corrs.append(corrs)
    average_corrs += np.array(corrs)


average_corrs /= num_files

# Calculate the variance for each point
for tau in range(maxtau - 1):
    mean_value = average_corrs[tau]
    variance = sum((np.array([corrs[tau] for corrs in all_corrs]) - mean_value)**2) / (num_files - 1)
    variances[tau] = variance

# Save the average_corrs and variances to a file
data_to_save = np.column_stack((range(1, maxtau), average_corrs, variances))
np.savetxt("correlation_data.txt", data_to_save, fmt="%d %f %f", header="i average_correlation variance")

