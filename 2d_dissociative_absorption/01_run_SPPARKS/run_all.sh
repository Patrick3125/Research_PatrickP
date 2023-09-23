rm -rf ../log
./run_multiple.sh
python ../02_parse_compute/correlation.py
python ../03_plot_data/plot_correlation.py
