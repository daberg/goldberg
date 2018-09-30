#!/bin/sh

PACKAGEPATH=`pwd`

# If running from scripts folder, change to parent directory
if echo $PACKAGEPATH | grep -q scripts; then
    PACKAGEPATH=`dirname $PACKAGEPATH`
fi

# If docker image not present, build it
if ! docker images | grep -q "goldberg-env"; then
    ${PACKAGEPATH}/scripts/docker-build.sh
fi

docker run                             \
    -it                                \
    -e "PYTHONPATH=/opt/goldberg"      \
    -e "GOLDBERGDEBUG=true"            \
    -w /opt/goldberg                   \
    -v "$PACKAGEPATH":/opt/goldberg    \
    goldberg-env python3 -m pdb $@
