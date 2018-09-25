import json
import matplotlib.pyplot as plt
import numpy as np
import sys


if len(sys.argv) != 2:
    print("Wrong number of arguments\n\n")
    print("USAGE:\n\tpython plot.py [FILEPATH]")
    sys.exit(1)

entries = []

with open(sys.argv[1], "r") as f:
    for line in f:
        entries.append(json.loads(line))

v = []
e = []
t = {}
m = {}

for entry in entries:
    num_vertices = entry[0]
    num_edges = (num_vertices * (num_vertices - 1)) / 2

    v.append(num_vertices)
    e.append(num_edges)

    for impl in entry[1]:
        name = impl[0]
        time = impl[1]['time']
        mem = impl[1]['memory']

        if name not in t:
            t[name] = []

        if name not in m:
            m[name] = []

        # Use implementation name as key
        t[name].append(time)
        m[name].append(mem)

for key in t:
    print(t[key])

for key in t:
    plt.plot(v, t[key])
plt.show()

for key in t:
    plt.plot(e, t[key])
plt.show()
