#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outvid=diss_ads.mp4
xhi=100
yhi=100
It=1.0
Rt=0.5
diffrate=30.0
# spparks executable
if [ ! -f $spkexe ]
then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

# generate sites data file "data.strips"
python create_site_file.py $xhi $yhi
#for diff in {1..80}
#do
  for seed in {1..10}
  do
    echo "** Starting run with seed $seed"
    
    #diffrate=$diff/2
    # execute spparks
    mpirun -np 1 $spkexe -in $spkscr -var seed $seed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -log log${seed}.spparks
    echo "** spparks run completed with seed $seed"

    # generate animated gif "diss_ads.gif"
    echo "** converting jpg files into an animated gif for seed $seed"
    #ffmpeg -y -framerate 30 -i dump.%05d.jpg diss_ads_${seed}.mp4
    echo "** animated gif for seed $seed will be shown"
  done
  python trial.py
#done
python difplot.py
