rm -rf ../log
rm -rf ../res
./run_multiple.sh
../02_parse_log/loop_SPPARKS_logs.sh
python ../03_surface_coverage/compute_av_surface_coverage.py
python ../03_surface_coverage/plot_all_cov.py
../04_correlation/loop_res_files.sh
python ../04_correlation/plot_correlation.py
python ../04_correlation/plot_log.py
