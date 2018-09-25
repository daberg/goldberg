#!/bin/bash

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
    -w /opt/goldberg                   \
    -v "$PACKAGEPATH":/opt/goldberg    \
    goldberg-env $@
