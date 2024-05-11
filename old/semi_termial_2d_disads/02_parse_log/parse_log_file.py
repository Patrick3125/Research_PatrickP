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
y_values = []


with open(input_file, "r") as f:
    lines = f.readlines()
    
    previous_line_is_data = False
    save_previous_line = None
    for line in lines:
        # Used Regular expressions to find lines with only 7 numbers
        real_data = re.match(r"\s*([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\deE.-]+)\s+(\d+)\s+(\d+)", line)
 
        if real_data:
            if previous_line_is_data:
                x_values.append(float(real_data.group(1)))
                y_values.append(float(real_data.group(7)))
                previous_line_is_data = False
            else:
                previous_line_is_data = True
                save_previous_line = real_data
        elif previous_line_is_data:
            x_values.append(float(save_previous_line.group(1)))
            y_values.append(float(save_previous_line.group(7)))
            previous_line_is_data = False

# Stack the two lists as columns
data = np.column_stack((x_values, y_values))

# Save the data to the output file in a two-column format
np.savetxt(output_file, data, fmt='%f', header="time covered_sites")

