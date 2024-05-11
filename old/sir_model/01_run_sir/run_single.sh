#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outvid=diss_ads.mp4
xhi=100
yhi=100
It=0.6
Rt=0.6
diffrate=72.0
seed=1
runtime=1000
Trun=0.1
size=$(( $xhi * $yhi ))

if [ ! -f $spkexe ]
then
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

# generate sites data file "data.strips"
python create_site_file.py $xhi $yhi


mpirun -np 1 $spkexe -in $spkscr -var seed $seed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -var runtime $runtime -var Trun $Trun -log log${seed}.spparks


python ../02_read_logs/parse.py "$It" "$Rt" "$diffrate" "$Trun" "$runtime"
python ../03_plot_data/sirGraph.py
