#! /bin/bash

source=$(dirname $0)
experiment_folder=$source/experiment_data/*/*

for folder in $(ls $experiment_folder -d); do
    if [[ -d $folder ]]; then
        echo "Running $folder"
        ./run.sh $folder > /dev/null
    fi
done

