rm -rf ../log
./run_multiple.sh
rm -rf ../res
python ../02_parse_log/loop_SPPARKS_logs.sh
python ../03_plot_data/plot_correlation.py
