#!/bin/bash

# Find the first directory that starts with "log" in the parent directory
logdir=$(find .. -maxdepth 1 -type d -name "log*" | sort | head -n 1)
if [ -z "$logdir" ]; then
    echo "Error: No directory starting with 'log' found"
    exit 1
fi

# Find the first directory that starts with "res" in the parent directory
resdir=$(find .. -maxdepth 1 -type d -name "res*" | sort | head -n 1)
if [ -z "$resdir" ]; then
    echo "Error: No directory starting with 'res' found"
    exit 1
fi

echo "Using log directory: $logdir"
echo "Using results directory: $resdir"

# Create correlation directory if it doesn't exist
if [ ! -d "$resdir" ]; then
    mkdir "$resdir"
fi

# Read Nruns from variables.txt
Nruns=$(grep -Po '"Nruns": *\K\d+' "$logdir/variables.txt")

# Loop through all res files in order
for (( i=1; i<=Nruns; i++ )); do
    res_file="$resdir/data${i}.txt"
    output_file="$resdir/corr${i}.txt"

    if [ -f "$res_file" ]; then
        python ../04_correlation/compute_correlation.py "$res_file" "$output_file" "$logdir" "$resdir"
    else
        echo "Error: Missing $res_file"
        exit 1
    fi
done

echo "Finished writing correlation.txt files"

python ../04_correlation/compute_av_correlation.py "$logdir" "$resdir"

echo "Finished writing average_correlation.txt."
