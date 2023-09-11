#!/bin/bash

spkexe=./spk_nonmui
spkscr=coldin.diss_ads
outvid=diss_ads.mp4
xhi=100
yhi=100
It=0.25
Rt=0.07142857142
diffrate=50
# spparks executable
if [ ! -f $spkexe ]
then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

#> diffrate.txt

# generate sites data file "data.strips"
python create_site_file.py $xhi $yhi
#for diff in {8..75}
  #diffrate=$(($diff*7+1))
  echo $diffrate >> diffrate.txt
  for three in {0..5}
  do
    for seed in {1..16}
    do
      chseed=$(($three*16+$seed))
      mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -log log${chseed}.spparks &
    done
    wait

  done
  python limt.py

#python difplot.py
#ffmpeg -y -framerate 60 -i dump.%05d.jpg diss_ads.mp4
