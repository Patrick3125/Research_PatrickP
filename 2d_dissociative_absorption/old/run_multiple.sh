#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outgif=diss_ads.mp4
#seed=1
xhi=300
yhi=300
rd=0.2
ra=0.3
total_runs=119 #total number of similations you want to run
runtime=10000
#../clean.sh
# spparks executable
if [ ! -f $spkexe ]
then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

python create_site_file.py $xhi $yhi

#runs the simulation in group of 16. 
for (( i=0; i<$total_runs; i+=16 )); do
        upper_limit=$(( $i + 16 < $total_runs ? $i + 16 : $total_runs ))

        for seed in $(seq $((i+1)) $upper_limit); do
          chseed=$(( $i + $seed ))
          mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var rd $rd -var ra $ra -var runtime $runtime -log log${seed}.spparks &
        done
        wait
      done


echo "rd=0.2 ra=0.3"
k=$(echo "$rd / $ra" | bc -l)
echo "k = rd/ra = $k"
theta=$(echo "1 / (1 + sqrt($k))" | bc -l)
echo "Theta_eq = 1/(1+sqrt(k)) = $theta"


python3 ../02_parse_compute/parse_compute.py "$rd" "$ra" "$runtime"
python3 ../03_plot_data/plot_correlation.py
