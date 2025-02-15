#!/bin/bash

spkexe=./spk_nonmui
spkscr=in.diss_ads
sitefile=site_data.2D_square
logdir=../log
outvid=vid.gif
xhi=500
yhi=500
k1=0.5 # O A -> A A
k2=0.3 # A B -> B B
k3=0.1 # B -> O
Nstep=1000
Nruns=1
deltat=1

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

seed=1
logfile=$logdir/log${seed}.spparks
echo "running $spkexe with seed = $seed"
mpirun -np 1 $spkexe -in $spkscr -log $logfile -screen none -var seed $seed -var xhi $xhi -var yhi $yhi -var sitefile $sitefile -var k1 $k1 -var k2 $k2 -var k3 $k3 -var Nstep $Nstep -var deltat $deltat &
wait

mv $sitefile $logdir
cp $spkscr $logdir

ffmpeg -y -framerate 10 -i dump.%05d.jpg $outvid
#animate $outvid &

#save all the variables into log folder using json format
echo "{" > $logdir/variables.txt
echo "  \"spkexe\": \"$spkexe\"," >> $logdir/variables.txt
echo "  \"spkscr\": \"$spkscr\"," >> $logdir/variables.txt
echo "  \"sitefile\": \"$sitefile\"," >> $logdir/variables.txt
echo "  \"logdir\": \"$logdir\"," >> $logdir/variables.txt
echo "  \"xhi\": $xhi," >> $logdir/variables.txt
echo "  \"yhi\": $yhi," >> $logdir/variables.txt
echo "  \"k1\": $k1," >> $logdir/variables.txt
echo "  \"k2\": $k2," >> $logdir/variables.txt
echo "  \"k3\": $k3," >> $logdir/variables.txt
echo "  \"Nstep\": $Nstep," >> $logdir/variables.txt
echo "  \"Nruns\": $Nruns," >> $logdir/variables.txt
echo "  \"deltat\": $deltat" >> $logdir/variables.txt
echo "}" >> $logdir/variables.txt
