import goldberg.benchmark
import graph_tool.generation
import json
import sys


def benchmark_complete_graph(num_vertices):
    print("Running benchmark on complete graph with {:d} vertices\n".format(num_vertices))

    g = graph_tool.generation.complete_graph(num_vertices, directed=True)
    capacity = g.new_edge_property("int")

    for edge in g.edges():
        capacity[edge] = 10

    return goldberg.benchmark.benchmark_all(g, g.vertex(0), g.vertex(1), capacity)


MAX_VERT = 100

if len(sys.argv) > 2:
    print("Wrong number of arguments\n\n")
    print("USAGE")
    print("\tpython completegraphs.py")
    print("\tpython completegraphs.py [MAX_VERT]")
    sys.exit(1)

if len(sys.argv) == 2:
    MAX_VERT = int(sys.argv[1])

with open('benchmark/results/complete_graph_results.dat', "w") as outfile:
    try :
        for i in range(2, MAX_VERT + 1):
            results = benchmark_complete_graph(i)

            print("Writing results to  complete_graph_results.dat\n\n\n")

            outfile.write("[{:d}, {:d}, ".format(i, int(i*(i-1)/2)) + json.dumps(results) + "]" + '\n')

        print("Completed benchmarks on complete graphs")

    except KeyboardInterrupt:
        print("Interrupted benchmark")
