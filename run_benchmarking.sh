#!/bin/bash

if [[ $1 == 'help' || $1 == '-h' || $1 == '--help' ]]
then
    echo "Usage:"
    echo "sh run_benchmarking.sh <tag> <repo> <input_type (csv or parquet)>"
    exit 0
fi

TAG=$1
REPO=$2
TYPE=$3

for filename in $REPO*.$TYPE; do python benchmarking.py -f $filename -t $TAG -r $REPO; done
