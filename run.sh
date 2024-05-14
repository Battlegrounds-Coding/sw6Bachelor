#! /bin/bash

source=$(dirname $0)
out_dir=$source/experiment_data_results/
dir=$1

experiment_name=$(basename $(realpath $dir/..))
experiment_dataset=$(basename $(realpath $dir/.))
name="${experiment_name}-${experiment_dataset}"

source $source/.venv/bin/activate

if ! [[ -d $out_dir ]]; then
    mkdir $out_dir
fi

if [[ -d $dir ]]; then
    echo "Running tests for project $name"
    python  $source/src/main.py \
        --rain=$dir/Rain.csv \
        --mode=headless \
        --data=$dir/DepthSensor.csv \
        --data-control=$dir/DepthControl.csv \
        --time=7000 \
        --name="$name" \
        --output="$out_dir/$name.csv" \
        --output-image="$out_dir/$name.pgf" \
        --show=true
else
    echo "'$dir' is not a directory"
fi


