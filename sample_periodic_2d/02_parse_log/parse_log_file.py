import numpy as np
import sys
import os
import json
import re

logdir = "../log"

if len(sys.argv) != 3:
    print("Usage: python parse_log_file.py <input_res_file> <output_file>")
    sys.exit(1)

# Read input file path and output file path from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Read input variables from the log directory's JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)

total_sites = var_data["xhi"] * var_data["yhi"]

x_values = []
spec1 = []
spec2 = []
spec3 = []
spec4 = []


with open(input_file, "r") as f:
    lines = f.readlines()
    
    previous_line_is_data = False
    save_previous_line = None
    for line in lines:
        # Use Regular expressions to find lines with only 10 numbers
        # Time    Naccept    Nreject    Nsweeps   CPU	vac	spec1 spec2 spec3 spec4
        real_data = re.match(r"\s*([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\deE.-]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
 
        # in case there are two consecutive lines with only 10 numbers, only store the later one. 
        if real_data:
            if previous_line_is_data:
                x_values.append(float(real_data.group(1)))
                spec1.append(float(real_data.group(7)))
                spec2.append(float(real_data.group(8)))
                spec3.append(float(real_data.group(9)))
                spec4.append(float(real_data.group(10)))

                previous_line_is_data = False
            else:
                previous_line_is_data = True
                save_previous_line = real_data
        elif previous_line_is_data:
            x_values.append(float(save_previous_line.group(1)))
            spec1.append(float(real_data.group(7)))
            spec2.append(float(real_data.group(8)))
            spec3.append(float(real_data.group(9)))
            spec4.append(float(real_data.group(10)))

            previous_line_is_data = False

# Stack the two lists as columns
data = np.column_stack((x_values, spec1, spec2, spec3, spec4))

# Save the data to the output file in a two-column format
np.savetxt(output_file, data, fmt='%f', header="time spec1 spec2 spec3 spec4")

