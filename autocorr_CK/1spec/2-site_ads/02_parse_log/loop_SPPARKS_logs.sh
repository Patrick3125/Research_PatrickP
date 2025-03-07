#!/bin/bash

logdir="../log"
resdir="../res"

# Check if the 'res' folder already exists
if [ -d "$resdir" ]; then
    echo "Error: $resdir directory already exists"
    exit 0
else
    mkdir $resdir
fi

# Extract Nrun from sim_params.txt
Nrun=$(grep '"Nrun"' $logdir/sim_params.txt | awk -F: '{print $2}' | tr -d ' ,')

# Find log files
log_files=($(find $logdir -name "log*.spparks"))

echo "** a total of ${#log_files[@]} log files detected"

if [ "$Nrun" -ne "${#log_files[@]}" ]; then
    echo "Error: Number of log files detected (${#log_files[@]}) does not match Nrun ($Nrun) from sim_params.txt!"
    exit 0
fi

#sort files so that it reads in order
readarray -t log_files < <(find $logdir -name log*.spparks | sort -V)

# Loop through the log files in order
for (( i=1; i<=Nrun; i++ )); do
    log_file=$logdir/log${i}.spparks
    data_file=$resdir/data${i}.txt
    surfcov_file=$resdir/surfcov${i}.txt
    
    if [ -f "$log_file" ]; then
        #echo "Processing $log_file -> $data_file"
        #python ../02_parse_log/parse_log_file.py "$log_file" "$data_file"
        echo "Processing $log_file -> $data_file, $surfcov_file"
        python ../02_parse_log/parse_log_file.py $log_file $data_file $surfcov_file
    else
        echo "Error: Missing $log_file"
        exit 0
    fi
done
