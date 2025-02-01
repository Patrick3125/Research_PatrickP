#!/bin/bash

rm -rf ../res
rm -rf ../log

for i in {1000..1000}; do
    size=$i

    ./run_multiple.sh $size
    ../02_parse_log/loop_SPPARKS_logs.sh

    if [ -d "../res" ]; then
        mv ../res ../res_$size
    fi

    if [ -d "../log" ]; then
        mv ../log ../log_$size
    fi


done
python ../03_surface_coverage/compute_av_surface_coverage.py
../04_correlation/loop_res_files.sh
#python ../03_surface_coverage/plot_theta.py
