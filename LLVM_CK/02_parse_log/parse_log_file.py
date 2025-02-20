import numpy as np
import sys
import os
import json
import re

logdir = "../log"

if len(sys.argv) == 3:
    comput_surfcov = False
elif len(sys.argv) == 4:
    comput_surfcov = True
else:
    print("Usage: python parse_log_file.py <input_res_file> <output_file> [<output_file2>]")
    sys.exit(0)

# Read input file path and output file path from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
if comput_surfcov:
    output_file2 = sys.argv[3]

# Read sim params from the log directory's JSON file
with open(os.path.join(logdir,'sim_params.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"]*var_data["yhi"]

x_values = []
y_values = []
z_values = []
if comput_surfcov:
    y2_values = []
    z2_values = []

with open(input_file,"r") as f:
    lines = f.readlines()
    
    previous_line_is_data = False
    save_previous_line = None
    for line in lines:
        # Use Regular expressions to find lines with only 8 numbers
        # Time    Naccept    Nreject    Nsweeps   CPU	vac	spec1 spec2
        real_data = re.match(r"\s*([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\deE.-]+)\s+(\d+)\s+(\d+)\s+(\d+)",line)
 
        # in case there are two consecutive lines with only 8 numbers, only store the later one. 
        if real_data:
            if previous_line_is_data:
                x_values.append(float(real_data.group(1)))
                y_values.append(float(real_data.group(7)))
                z_values.append(float(real_data.group(8)))
                if comput_surfcov:
                    y2_values.append(float(real_data.group(7))/total_sites)
                    z2_values.append(float(real_data.group(8))/total_sites)
                previous_line_is_data = False
            else:
                previous_line_is_data = True
                save_previous_line = real_data
        elif previous_line_is_data:
            x_values.append(float(save_previous_line.group(1)))
            y_values.append(float(save_previous_line.group(7)))
            z_values.append(float(save_previous_line.group(8)))
            if comput_surfcov:
                y2_values.append(float(save_previous_line.group(7))/total_sites)
                z2_values.append(float(save_previous_line.group(8))/total_sites)
            previous_line_is_data = False

# First output file
# Stack the two lists as columns
data = np.column_stack((x_values,y_values,z_values))
# Save the data to the output file in a two-column format
np.savetxt(output_file,data,fmt='%f',header="time\tspec1 cnt\tspec2 cnt")

# Second output file
if comput_surfcov:
    surfcov = np.column_stack((x_values,y2_values,z2_values))
    np.savetxt(output_file2,surfcov,fmt='%e',header="time\tsurfcov1\tsurfcov2")
