#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outvid=diss_ads.mp4
xhi=100
yhi=100
It=0.4
Rt=0.3
diffrate=10.0
total_runs=21               # number of simulations you want to run
Rt_iter=0                   # number of timestimes you want to loop over different Rt values
It_iter=0                   # number of times you want to loop over different It values
diffrate_iter=3             # number of times you want to loop over different diffrate values
runtime=500
Trun=0.1
# Check for spparks executable
if [ ! -f $spkexe ]; then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

#clean logfiles from previous runs.
cd ..
./clean.sh
cd 01_run_sir
../clean.sh
> ../ode_params.txt

# Generate sites data file "data.strips"
python create_site_file.py $xhi $yhi

increment=0.05 #increment when running different rt, it, dt runs

for rt in $(seq $Rt $increment $(echo "$Rt_iter*$increment+$Rt" | bc)); do
  for it in $(seq $It $increment $(echo "$It_iter*$increment+$It" | bc)); do
    for diff in $(seq $diffrate $increment $(echo "$diffrate_iter*$increment+$diffrate" | bc)); do
      for (( i=0; i<$total_runs; i+=8 )); do
        upper_limit=$(( $i + 8 < $total_runs ? $i + 8 : $total_runs ))

        for seed in $(seq $((i+1)) $upper_limit); do
          chseed=$(( $i + $seed ))
          mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $it -var Rt $rt -var diffrate $diff -var runtime $runtime -var Trun $Trun -log log${seed}.spparks &
        done
        wait
      done
      python ../02_read_logs/parse.py "$it" "$rt" "$diff" "$Trun" "$runtime"
    done
  done
done
if [ "$Rt_iter" -gt 0 ]; then
  python ../03_plot_data/plotk.py
fi
if [ "$diffrate_iter" -gt 0 ]; then
  python ../03_plot_data/diffrate.py
fi
#python ../03_plot_data/sirGraph.py

