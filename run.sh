#! /bin/bash

source=$(dirname $0)
dir=$1

source $source/.venv/bin/activate

if [ -d $dir ]; then
    echo "Running tests for project $dir"
    python  $source/src/main.py \
        --rain=$dir/data/fixed/RainData.csv \
        --mode=headless \
        --data=$dir/data/fixed/DepthDataFixed.csv \
        --data-control=$dir/data/optimal/DepthDataOptimal.csv \
        --time=7000
else
    echo "'$dir' is not a directory"
fi


