#!/bin/bash

spkexe=./spk_nonmui
outvid=diss_ads.gif
spkscr=in.diss_ads_gif
sitefile=site_data.2D_square
logdir=../log
seed=1
xhi=5
yhi=5
rd2=2.5
ra2=0.5
Nruns=500
Nstep=100
deltat=0.01

# check spparks executable
if [ ! -f $spkexe ]
then
    echo "ERROR: spparks executable $exec1 not found"
    echo "1. go to ~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI"
    echo "2. make nonmui"
    exit
fi

# check log dir
if [ -d $logdir ]
then
    echo "ERROR: $logdir already exists"
    exit
else
    mkdir $logdir
fi

python create_site_file.py $xhi $yhi $sitefile

#runs the simulation in group of 16. 
        logfile=$logdir/log${seed}.spparks
        echo "running $spkexe with seed = $seed"
        mpirun -np 1 $spkexe -in $spkscr -log $logfile -var seed $seed -var xhi $xhi -var yhi $yhi -var sitefile $sitefile -var rd2 $rd2 -var ra2 $ra2 -var Nstep $Nstep -var deltat $deltat 

mv $sitefile $logdir
cp $spkscr $logdir

#save all the variables into log folder using json format
echo "{" > $logdir/variables.txt
echo "  \"spkexe\": \"$spkexe\"," >> $logdir/variables.txt
echo "  \"spkscr\": \"$spkscr\"," >> $logdir/variables.txt
echo "  \"sitefile\": \"$sitefile\"," >> $logdir/variables.txt
echo "  \"logdir\": \"$logdir\"," >> $logdir/variables.txt
echo "  \"xhi\": $xhi," >> $logdir/variables.txt
echo "  \"yhi\": $yhi," >> $logdir/variables.txt
echo "  \"rd2\": $rd2," >> $logdir/variables.txt
echo "  \"ra2\": $ra2," >> $logdir/variables.txt
echo "  \"Nruns\": $Nruns," >> $logdir/variables.txt
echo "  \"Nstep\": $Nstep," >> $logdir/variables.txt
echo "  \"deltat\": $deltat" >> $logdir/variables.txt
echo "}" >> $logdir/variables.txt
echo "** animated gif will be shown"

ffmpeg -y -framerate 2 -i dump.%05d.jpg $outvid
animate $outvid &


