import json
import matplotlib.pyplot as plt
import sys


MIN_SAMPLES = 0
entries = []
implementations = {}

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print("Wrong number of arguments\n\n")
    print("USAGE")
    print("\tpython plot.py [FILEPATH]")
    print("\tpython plot.py [FILEPATH] [MIN_SAMPLES]")
    sys.exit(1)

if len(sys.argv) == 3:
    MIN_SAMPLES = int(sys.argv[2])

# Read target JSON file
with open(sys.argv[1], "r") as f:
    for line in f:
        entries.append(json.loads(line))

# Parse data
for entry in entries:
    num_vertices = entry[0]
    num_edges = entry[1]

    for impl in entry[2]:
        name = impl[0]
        time = impl[1]['time']
        mem = impl[1]['memory']

        if name not in implementations:
            implementations[name] = {
                "tv" : {},
                "te" : {},
                "mv" : {},
                "me" : {}
            }

        if time != 0:
            if num_vertices not in implementations[name]["tv"]:
                implementations[name]["tv"][num_vertices] = []
            implementations[name]["tv"][num_vertices].append(time)

            if num_edges not in implementations[name]["te"]:
                implementations[name]["te"][num_edges] = []
            implementations[name]["te"][num_edges].append(time)

        if mem != 0:
            if num_vertices not in implementations[name]["mv"]:
                implementations[name]["mv"][num_vertices] = []
            implementations[name]["mv"][num_vertices].append(mem)

            if num_edges not in implementations[name]["me"]:
                implementations[name]["me"][num_edges] = []
            implementations[name]["me"][num_edges].append(mem)

# Delete entries with insufficient number of samples
for impl in implementations:
    for num_vertices in list(implementations[impl]["tv"].keys()):
        if len(implementations[impl]["tv"][num_vertices]) < MIN_SAMPLES:
            del implementations[impl]["tv"][num_vertices]

    for num_edges in list(implementations[impl]["te"].keys()):
        if len(implementations[impl]["te"][num_edges]) < MIN_SAMPLES:
            del implementations[impl]["te"][num_edges]

    for num_vertices in list(implementations[impl]["mv"].keys()):
        if len(implementations[impl]["mv"][num_vertices]) < MIN_SAMPLES:
            del implementations[impl]["mv"][num_vertices]

    for num_edges in list(implementations[impl]["me"].keys()):
        if len(implementations[impl]["me"][num_edges]) < MIN_SAMPLES:
            del implementations[impl]["me"][num_edges]

# Reduce to average
for impl in implementations:
    for num_vertices in implementations[impl]["tv"]:
        implementations[impl]["tv"][num_vertices] = (
            sum(implementations[impl]["tv"][num_vertices])
            / len(implementations[impl]["tv"][num_vertices])
        )

    for num_edges in implementations[impl]["te"].keys():
        implementations[impl]["te"][num_edges] = (
            sum(implementations[impl]["te"][num_edges])
            / len(implementations[impl]["te"][num_edges])
        )

    for num_vertices in implementations[impl]["mv"]:
        implementations[impl]["mv"][num_vertices] = (
            sum(implementations[impl]["mv"][num_vertices])
            / len(implementations[impl]["mv"][num_vertices])
        )

    for num_edges in implementations[impl]["me"]:
        implementations[impl]["me"][num_edges] = (
            sum(implementations[impl]["me"][num_edges])
            / len(implementations[impl]["me"][num_edges])
        )

# Plot time against number of vertices
for impl in implementations:
    sorted_pairs = sorted(implementations[impl]["tv"].items(), key=lambda kv : kv[0])
    x = [pair[0] for pair in sorted_pairs]
    y = [pair[1] for pair in sorted_pairs]
    plt.plot(x, y, "o")
plt.legend(implementations.keys())
plt.xlabel("Number of vertices")
plt.ylabel("Average execution time (ms)")
plt.show()

# Plot time against number of edges
for impl in implementations:
    sorted_pairs = sorted(implementations[impl]["te"].items(), key=lambda kv : kv[0])
    x = [pair[0] for pair in sorted_pairs]
    y = [pair[1] for pair in sorted_pairs]
    plt.plot(x, y, "o")
plt.legend(implementations.keys())
plt.xlabel("Number of edges")
plt.ylabel("Average execution time (ms)")
plt.show()

# Plot memory against number of vertices
for impl in implementations:
    sorted_pairs = sorted(implementations[impl]["mv"].items(), key=lambda kv : kv[0])
    x = [pair[0] for pair in sorted_pairs]
    y = [pair[1] for pair in sorted_pairs]
    plt.plot(x, y, "o")
plt.legend(implementations.keys())
plt.xlabel("Number of vertices")
plt.ylabel("Average memory usage (KiB)")
plt.show()

# Plot memory against number of edges
for impl in implementations:
    sorted_pairs = sorted(implementations[impl]["me"].items(), key=lambda kv : kv[0])
    x = [pair[0] for pair in sorted_pairs]
    y = [pair[1] for pair in sorted_pairs]
    plt.plot(x, y, "o")
plt.legend(implementations.keys())
plt.xlabel("Number of edges")
plt.ylabel("Average memory usage (KiB)")
plt.show()
