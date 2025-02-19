import numpy as np
import sys
import os
import json
import re
logdir = "../log"
if len(sys.argv) != 4:
    print("Usage: python parse_log_file.py <input_res_file> <output_file> <surcov_file>")
    sys.exit(0)
# Read input file path and output file path from arguments
input_file = sys.argv[1]
output_file = sys.argv[2]
surcov_file = sys.argv[3]
# Read input variables from the log directory's JSON file
with open(os.path.join(logdir, 'variables.txt')) as f:
    var_data = json.load(f)
total_sites = var_data["xhi"] * var_data["yhi"]
t_val = []
A_val = []
B_val = []
A_cov = []
B_cov = []
O_val = []
O_cov = []
with open(input_file, "r") as f:
    lines = f.readlines()
    
    previous_line_is_data = False
    save_previous_line = None
    for line in lines:
        # Use Regular expressions to find lines with only 8 numbers
        # Time    Naccept    Nreject    Nsweeps   CPU	vac	spec1 spec2 
        real_data = re.match(r"\s*([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s+([\deE.-]+)\s+(\d+)\s+(\d+)\s+(\d+)", line)
 
        # in case there are two consecutive lines with only 7 numbers, only store the later one. 
        if real_data:
            if previous_line_is_data:
                t_val.append(float(real_data.group(1)))
                A_val.append(float(real_data.group(7)))
                B_val.append(float(real_data.group(8)))
                A_cov.append(float(real_data.group(7))/total_sites)
                B_cov.append(float(real_data.group(8))/total_sites)
                O_val.append(float(real_data.group(6)))
                O_cov.append(float(real_data.group(6))/total_sites)
                previous_line_is_data = False
            else:
                previous_line_is_data = True
                save_previous_line = real_data
        elif previous_line_is_data:
            t_val.append(float(save_previous_line.group(1)))
            A_val.append(float(save_previous_line.group(7)))
            B_val.append(float(save_previous_line.group(8)))
            A_cov.append(float(save_previous_line.group(7))/total_sites)
            B_cov.append(float(save_previous_line.group(8))/total_sites)
            O_val.append(float(save_previous_line.group(6)))
            O_cov.append(float(save_previous_line.group(6))/total_sites)
            previous_line_is_data = False
# Stack the two lists as columns
data = np.column_stack((t_val, O_val, A_val, B_val))
# Save the data to the output file in a two-column format
np.savetxt(output_file, data, fmt='%f', header="time O A B")
data = np.column_stack((t_val, O_cov, A_cov, B_cov))
np.savetxt(surcov_file, data, fmt='%f', header="time O/N A/N B/N")
