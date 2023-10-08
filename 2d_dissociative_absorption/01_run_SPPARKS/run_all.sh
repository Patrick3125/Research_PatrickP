rm -rf ../log
rm -rf ../res
./run_multiple.sh
../02_parse_log/loop_SPPARKS_logs.sh
../04_correlation/loop_res_files.sh
python ../04_correlation/plot_correlation.py
python ../04_correlation/plot_log.py
