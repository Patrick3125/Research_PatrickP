#!/bin/bash

spkexe=~/GIT/FHDeX/exec/compressible_stag_mui/SPPARKS_MUI/spk_nonmui
spkscr=in.LLVM
sitefile=site_data.2D_square
logdir=../log

xhi=100
yhi=100
k1=0.5      # O + A -> A + A
k2=0.3      # A + B -> B + B
k3=0.1      # B -> O
Nrun=400
Nstep=1000
deltat=1.0

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

# run each batch of 16 simulations
for (( i=0; i<$Nrun; i+=8 ))
do
    imax=$(( $i + 8 < $Nrun ? $i + 8 : $Nrun ))

    for seed in $(seq $((i+1)) $imax)
    do
        logfile=$logdir/log${seed}.spparks
        echo "running $spkexe with seed = $seed"
        mpirun -np 1 $spkexe -in $spkscr -log $logfile -screen none -var seed $seed -var xhi $xhi -var yhi $yhi -var sitefile $sitefile -var k1 $k1 -var k2 $k2 -var k3 $k3 -var Nstep $Nstep -var deltat $deltat &
    done
    wait
done

mv $sitefile $logdir
cp $spkscr $logdir

# save all sim params into log dir using json format
echo "{" > $logdir/sim_params.txt
echo "  \"spkexe\": \"$spkexe\"," >> $logdir/sim_params.txt
echo "  \"spkscr\": \"$spkscr\"," >> $logdir/sim_params.txt
echo "  \"sitefile\": \"$sitefile\"," >> $logdir/sim_params.txt
echo "  \"logdir\": \"$logdir\"," >> $logdir/sim_params.txt
echo "  \"xhi\": $xhi," >> $logdir/sim_params.txt
echo "  \"yhi\": $yhi," >> $logdir/sim_params.txt
echo "  \"k1\": $k1," >> $logdir/sim_params.txt
echo "  \"k2\": $k2," >> $logdir/sim_params.txt
echo "  \"k3\": $k3," >> $logdir/sim_params.txt
echo "  \"Nrun\": $Nrun," >> $logdir/sim_params.txt
echo "  \"Nstep\": $Nstep," >> $logdir/sim_params.txt
echo "  \"deltat\": $deltat" >> $logdir/sim_params.txt
echo "}" >> $logdir/sim_params.txt
