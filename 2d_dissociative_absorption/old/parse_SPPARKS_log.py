import numpy as np
import math
import sys
import os
import json
import re

logdir = "../log"
resdir = "../res"

# Create the folder to save computed data if it doesn't exist
if not os.path.exists(resdir):
    os.makedirs(resdir)

#read input variables from json file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"] * var_data["yhi"]
rd2 = var_data["rd2"]
ra2 = var_data["ra2"]
Nruns = var_data["Nruns"]
Nstep = var_data["Nstep"]
deltat = var_data["deltat"]

#find log files
log_files = [f for f in os.listdir(logdir) if f.startswith('log') and f.endswith('.spparks')]

print("** a total of %d log files detected" % (len(log_files)))

# Loop through all log files
for i in range(1, Nruns+1):
    x_values = []
    y_values = []
    filename = os.path.join(logdir, "log{}.spparks".format(i))
    print("reading %s" % filename)

    with open(filename, "r") as f:
        lines = f.readlines()
        
        previous_line_is_data = False
        save_previous_line = None

        for line in lines:

            #only read second line when there are two lines after each other
        
            # Used Regular expressions to find lines with only 7 numbers
            real_data = re.match(r"\s*([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)", line)
            
            if real_data:
                if previous_line_is_data:
                    x_values.append(float(real_data.group(1)))
                    y_values.append(float(real_data.group(7)) / total_sites)
                    previous_line_is_data = False
                else:
                    previous_line_is_data = True
                    save_previous_line = real_data
            elif previous_line_is_data:
                x_values.append(float(save_previous_line.group(1)))
                y_values.append(float(save_previous_line.group(7)) / total_sites)
                previous_line_is_data = False
