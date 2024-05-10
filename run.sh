#! /bin/bash

source=$(dirname $0)
dir=$1

source $source/.venv/bin/activate

if [ -d $dir ]; then
    echo "Running tests for project $dir"
    dir=$dir python  $source/src/main.py \
        --rain=$dir/Rain.csv \
        --mode=headless \
        --data=$dir/DepthSensor.csv \
        --data-control=$dir/DepthControl.csv \
        --time=7000
else
    echo "'$dir' is not a directory"
fi


