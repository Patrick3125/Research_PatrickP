rm -rf ../log
./run_multiple.sh
rm -rf ../res
python ../02_parse_log/loop_SPPARKS_logs.sh
python ../03_stats/loop_res_files.sh
python ../04_plot_data/plot_correlation.py

