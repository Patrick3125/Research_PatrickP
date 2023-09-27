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


# Loop through the log files in order using Nruns
for (( i=1; i<=Nruns; i++ )); do
    log_file="$logdir/log${i}.spparks"
    res_file="$resdir/res${i}.txt"
    
    if [ -f "$log_file" ]; then
        echo "Processing $log_file -> $res_file"
        python ../02_parse_log/parse_log_file.py "$log_file" "$res_file"
    else
        echo "Error: Missing $log_file"
    fi
done
echo "Finished Writing res files"
