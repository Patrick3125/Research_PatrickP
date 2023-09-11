#!/bin/bash

# --- Initial Variables ---
spkexe=./spk_nonmui
spkscr=in.diss_ads
outvid=diss_ads.mp4
xhi=20
yhi=20
It=0.4
Rt=0.3
diffrate=10.0
total_runs=17               # number of simulations you want to run
Rt_iter=0                   # number of timestimes you want to loop over different Rt values
It_iter=0                   # number of times you want to loop over different It values
diffrate_iter=0             # number of times you want to loop over different diffrate values
run_time=100
# Check for spparks executable
if [ ! -f $spkexe ]; then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

# Reset diffrate.txt
> diffrate.txt

./clean.sh

# Generate sites data file "data.strips"
python create_site_file.py $xhi $yhi

increment=0.05

for rt in $(seq $Rt $increment $(echo "$Rt_iter*$increment+$Rt" | bc)); do
  for it in $(seq $It $increment $(echo "$It_iter*$increment+$It" | bc)); do
    for diff in $(seq $diffrate $increment $(echo "$diffrate_iter*$increment+$diffrate" | bc)); do
      echo $rt $it $diff >> diffrate.txt
      for (( i=0; i<$total_runs; i+=16 )); do
        upper_limit=$(( $i + 16 < $total_runs ? $i + 16 : $total_runs ))

        for seed in $(seq $((i+1)) $upper_limit); do
          chseed=$(( $i + $seed ))
          mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $it -var Rt $rt -var diffrate $diff -var run_time $run_time -log log${seed}.spparks &
        done
        wait
      done
      python ../03_plot_data/findk.py
    done
  done
done

python ../03_plot_data/plotk.py
#ffmpeg -y -framerate 60 -i dump.%05d.jpg diss_ads.mp4

