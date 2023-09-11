#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outvid=diss_ads.mp4
xhi=100
yhi=100
It=0.3
Rt=0.3
diffrate=72.0
seed=1
# spparks executable
if [ ! -f $spkexe ]
then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

> diffrate.txt

# generate sites data file "data.strips"
python create_site_file.py $xhi $yhi
mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -log log${chseed}.spparks
#python limt.py
#done
#python difplot.py
#ffmpeg -y -framerate 60 -i dump.%05d.jpg diss_ads.mp4
