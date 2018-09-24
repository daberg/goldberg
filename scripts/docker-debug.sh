#!/bin/sh

PACKAGEPATH=`pwd`

# If running from scripts folder, change to parent directory
if echo $PACKAGEPATH | grep -q scripts; then
    PACKAGEPATH=`dirname $PACKAGEPATH`
fi

docker run                             \
    -it                                \
    -e "PYTHONPATH=/opt/goldberg"      \
    -e "GOLDBERGDEBUG=true"            \
    -w /opt/goldberg                   \
    -v "$PACKAGEPATH":/opt/goldberg    \
    tiagopeixoto/graph-tool python3 -m pdb goldberg/main.py
