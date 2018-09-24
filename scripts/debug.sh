#!/bin/sh
docker run -it -w /opt/goldberg -v $(pwd):/opt/goldberg tiagopeixoto/graph-tool python3 -m pdb main.py
