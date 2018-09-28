#!/bin/bash

PACKAGEPATH=`pwd`

# If running from scripts folder, change to parent directory
if echo $PACKAGEPATH | grep -q scripts; then
    PACKAGEPATH=`dirname $PACKAGEPATH`
fi

echo "Building docker image for goldberg package"
docker build -t goldberg-env "$PACKAGEPATH"
