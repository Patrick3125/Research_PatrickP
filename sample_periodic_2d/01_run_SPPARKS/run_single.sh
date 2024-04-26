#!/bin/bash

spkexe=./spk_nonmui
outvid=diss_ads.gif
spkscr=in.diss_ads
sitefile=site_data.2D_square
logdir=../log
seed=1
xhi=5
yhi=5
raA1=0.5
rdA1=2.5
raB1=0.5
rdB1=2.5
raX2=0.5
rdX2=2.5
raY2=0.5
rdY2=2.5
Nstep=100
Nruns=1
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
logfile=$logdir/log${seed}.spparks
mpirun -np 1 $spkexe -in $spkscr -log $logfile -var seed $seed -var raA1 $raA1 -var rdA1 $rdA1 -var raB1 $raB1 -var rdB1 $rdB1 -var raX2 $raX2 -var rdX2 $rdX2 -var raY2 $raY2 -var rdY2 $rdY2 -var xhi $xhi -var yhi $yhi -var sitefile $sitefile -var Nstep $Nstep -var deltat $deltat

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
echo "  \"raA1\": $raA1," >> $logdir/variables.txt
echo "  \"rdA1\": $rdA1," >> $logdir/variables.txt
echo "  \"raB1\": $raA1," >> $logdir/variables.txt
echo "  \"rdB1\": $rdA1," >> $logdir/variables.txt
echo "  \"raX2\": $raA1," >> $logdir/variables.txt
echo "  \"rdX2\": $rdA1," >> $logdir/variables.txt
echo "  \"raY2\": $raA1," >> $logdir/variables.txt
echo "  \"rdY2\": $rdA1," >> $logdir/variables.txt
echo "  \"Nruns\": $Nruns," >> $logdir/variables.txt
echo "  \"Nstep\": $Nstep," >> $logdir/variables.txt
echo "  \"deltat\": $deltat" >> $logdir/variables.txt
echo "}" >> $logdir/variables.txt
echo "** animated gif will be shown"

# Make video from image outputs
#ffmpeg -y -framerate 2 -i dump.%05d.jpg $outvid
#animate $outvid &


