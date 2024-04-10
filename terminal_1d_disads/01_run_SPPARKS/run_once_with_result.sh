#!/bin/bash

rm -rf ../res
rm -rf ../log
    ./run_multiple.sh 13
    ../02_parse_log/loop_SPPARKS_logs.sh
    python ../03_surface_coverage/compute_av_surface_coverage.py
python ../03_surface_coverage/plot_all_cov.py
