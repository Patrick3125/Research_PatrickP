#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outvid=diss_ads.mp4
xhi=100
yhi=100
It=0.4
Rt=0.3
diffrate=50.0
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
#for diff in {8..75}
for ks in {1..13}
do
  someconstant=14
  Rt=$(echo "scale=2; $ks / $someconstant" | bc)
  echo $Rt >> diffrate.txt
  for three in {1..8}
  do
    for seed in {1..16}
    do
      chseed=$(($three*48+$seed))
      mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -log log${seed}.spparks &
    done
    wait

    for seed in {17..32}
    do
      chseed=$(($three*32+$seed))
      mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -log log${seed}.spparks &
    done
    wait
    
    for seed in {33..48}
    do
      chseed=$(($three*32+$seed))
      mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var It $It -var Rt $Rt -var diffrate $diffrate -log log${seed}.spparks &
    done
    wait

    python findk.py
  done
done
python plotk.py
#ffmpeg -y -framerate 60 -i dump.%05d.jpg diss_ads.mp4
