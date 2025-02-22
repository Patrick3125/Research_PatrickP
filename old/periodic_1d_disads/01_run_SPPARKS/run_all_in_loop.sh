#!/bin/bash

rm -rf ../res
rm -rf ../log

for i in {3..20}; do
    size=$i

    ./run_multiple_with_input.sh $size
    ../02_parse_log/loop_SPPARKS_logs.sh
    python ../03_surface_coverage/compute_av_surface_coverage.py

    if [ -d "../res" ]; then
        mv ../res ../res_$size
    fi

    if [ -d "../log" ]; then
        mv ../log ../log_$size
    fi


done
python ../03_surface_coverage/plot_theta.py
