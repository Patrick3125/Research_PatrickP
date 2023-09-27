rm -rf ../log
./run_multiple.sh
rm -rf ../res
rm -rf ../correlation
../02_parse_log/loop_SPPARKS_logs.sh
../03_stats/loop_res_files.sh
python ../04_plot_data/plot_correlation.py

