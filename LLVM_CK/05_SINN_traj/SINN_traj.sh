#!/bin/bash

TRAJDIR=../traj

NTRAJ=400
NTPT=400
FREQ=1

if [ -d $TRAJDIR ]
then
    echo ERROR: $TRAJDIR already exists
    exit
fi 

mkdir $TRAJDIR

python SINN_traj.py $NTRAJ $NTPT $FREQ
