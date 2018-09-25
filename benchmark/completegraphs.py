import goldberg.benchmark
import graph_tool.generation
import json


def benchmark_complete_graph(num_vertices):
    print("Running benchmark on complete graph with {:d} vertices\n".format(num_vertices))

    g = graph_tool.generation.complete_graph(num_vertices, directed=True)
    capacity = g.new_edge_property("int")

    for edge in g.edges():
        capacity[edge] = 5

    return goldberg.benchmark.benchmark_all(g, g.vertex(0), g.vertex(1), capacity)

with open('benchmark/results/complete_graph_results.dat', "w") as outfile:
    try :
        for i in range(2, 150):
            results = benchmark_complete_graph(i)

            print("Writing results to  complete_graph_results.dat\n\n\n")

            outfile.write("[{:d}, ".format(i) + json.dumps(results) + "]" + '\n')

    except KeyboardInterrupt:
        print("Interrupted")

print("Completed benchmarks on complete graphs")
