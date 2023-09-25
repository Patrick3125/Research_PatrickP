#!/bin/bash

logdir="../log"
resdir="../res"

# Check if the 'res' folder already exists
if [ -d "$resdir" ]; then
    echo "Error: $resdir  directory already exists"
    exit 1
else
    mkdir "$resdir"
fi

# Extract Nruns from variables.txt
Nruns=$(grep '"Nruns"' $logdir/variables.txt | awk -F: '{print $2}' | tr -d ' ,')

# Find log files
log_files=($(find $logdir -name "log*.spparks"))

echo "** a total of ${#log_files[@]} log files detected"

if [ "$Nruns" -ne "${#log_files[@]}" ]; then
    echo "Error: Number of log files detected (${#log_files[@]}) does not match Nruns ($Nruns) from variables.txt!"
    exit 1
fi

readarray -t log_files < <(find $logdir -name "log*.spparks" | sort -V)


# Loop through all log files
for log_file in "${log_files[@]}"; do
    # Extract the numbering from the log_file name, assuming the naming format is log<num>.spparks
    num=$(basename "$log_file" | sed 's/^log\([0-9]*\)\.spparks$/\1/')
    
    # Construct the res_file path
    res_file="$resdir/res$num.txt"
    
    echo "Processing $log_file -> $res_file"
    python parse_log_file.py "$log_file" "$res_file"
done

