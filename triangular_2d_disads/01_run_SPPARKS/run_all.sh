#!/bin/bash

rm -rf ../res
rm -rf ../log

for x in {1..3}; do
    for y in {1..3}; do
        size_x=$x
        size_y=$y

        ./run_multiple.sh $size_x $size_y
        ../02_parse_log/loop_SPPARKS_logs.sh
        python ../03_surface_coverage/compute_av_surface_coverage.py

        if [ -d "../res" ]; then
            mv ../res ../res_${size_x}_${size_y}
        fi

        if [ -d "../log" ]; then
            mv ../log ../log_${size_x}_${size_y}
        fi
    done

done

python ../03_surface_coverage/plot_theta.py
