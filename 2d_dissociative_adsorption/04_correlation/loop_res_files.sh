#!/bin/bash

logdir="../log"
resdir="../res"

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

