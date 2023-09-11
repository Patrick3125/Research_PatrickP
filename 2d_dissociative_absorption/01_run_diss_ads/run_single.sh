#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
outgif=diss_ads.mp4
#seed=1
xhi=300
yhi=300
rd=0.2
ra=0.3
./clean.sh
# spparks executable
if [ ! -f $spkexe ]
then
  echo "ERROR: spparks executable $exec1 not found"
  echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
  echo "2. make nonmui"
  exit
fi

python create_site_file.py $xhi $yhi


for seed in {0..31}
do
	for seed2 in {0..15} 
	do
	chseed=$(echo "$seed*16+$seed2+1" | bc)
	mpirun -np 1 $spkexe -in $spkscr -var seed $chseed -var xhi $xhi -var yhi $yhi -var rd $rd -var ra $ra -log log${chseed}.spparks &
	done
	wait
done
wait


echo "rd=0.2 ra=0.3"
k=$(echo "$rd / $ra" | bc -l)
echo "k = rd/ra = $k"
theta=$(echo "1 / (1 + sqrt($k))" | bc -l)
echo "Theta_eq = 1/(1+sqrt(k)) = $theta"

#animate $outgif & 
#python graph.py
python cor1.py "$rd" "$ra"
