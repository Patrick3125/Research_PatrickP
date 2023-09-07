#!/bin/bash

# infection rates
for It in 0.5 0.7 0.9 1.1 1.3 1.5
do
    # recovery rates
    for Rt in 0.01 0.02 0.03 0.04 0.05
    do
        bash run_single.sh $It $Rt
    done
done
