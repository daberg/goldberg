#!/bin/bash

PACKAGEPATH=`pwd`

# If running from scripts folder, change to parent directory
if echo $PACKAGEPATH | grep -q scripts; then
    PACKAGEPATH=`dirname $PACKAGEPATH`
fi

for BENCH in $PACKAGEPATH/benchmark/*.py; do
    # Handle no matches
    if [ ! -e "$BENCH" ]; then
        echo "No benchmark tests found at ${PACKAGEPATH}/benchmark"
        echo "Calling from wrong directory?"
        exit 1
    fi

    # Run benchmark
    BENCHNAME=$(basename "$BENCH")
    echo "Running benchmark: ${BENCHNAME}"
    python3 $BENCH || echo "Benchmark $BENCHNAME exited with an error"
    printf "\n\n"
done
