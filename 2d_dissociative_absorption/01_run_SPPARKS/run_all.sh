rm -rf ../log
rm -rf ../res
rm -rf ../correlation
./run_multiple.sh
../02_parse_log/loop_SPPARKS_logs.sh
../03_stats/loop_res_files.sh
python ../04_plot_data/plot_correlation.py
python ../04_plot_data/plot_log.py
