#!/bin/bash

logdir="../log"
resdir="../res"
corrdir="../correlation"

# Create correlation directory if it doesn't exist
if [ ! -d "$corrdir" ]; then
    mkdir "$corrdir"
fi

# Read Nruns from variables.txt
Nruns=$(grep -Po '"Nruns": *\K\d+' "$logdir/variables.txt")

# Loop through all res files in order
for (( i=1; i<=Nruns; i++ )); do
    res_file="$resdir/res${i}.txt"
    output_file="$corrdir/correlation${i}.txt"

    if [ -f "$res_file" ]; then
        python ../03_stats/compute_correlation.py "$res_file" "$output_file"
    else
        echo "Error: Missing $res_file"
        exit 1
    fi
done

echo "Finished writing correlation.txt files"

python ../03_stats/compute_av_correlation.py

echo "Finished writing average_correlation.txt."

