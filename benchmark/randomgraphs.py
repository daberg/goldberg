import goldberg.benchmark
import graph_tool.generation
import graph_tool.topology
import json
import pickle
import random
import sys


def generate_random_graph(num_vertices):
    g = graph_tool.generation.random_graph(
        num_vertices,
        lambda : (random.randint(1, num_vertices - 1), random.randint(1, num_vertices - 1)),
        directed=True
    )

    capacity = g.new_edge_property("int")
    for edge in g.edges():
        capacity[edge] = random.randint(1, 50)

    return g, capacity


MAX_VERT = 100
NUM_ITER = 25

if len(sys.argv) != 1 and len(sys.argv) != 3:
    print("Wrong number of arguments\n\n")
    print("USAGE")
    print("\tpython randomgraphs.py")
    print("\tpython randomgraphs.py [MAX_VERT] [NUM_ITER]")
    sys.exit(1)

if len(sys.argv) == 3:
    MAX_VERT = int(sys.argv[1])
    NUM_ITER = int(sys.argv[2])

f_res = open('benchmark/results/random_graph_results.dat', "w")
f_graphs = open('benchmark/results/random_graphs.dat', "wb")

try:
    for num_vertices in range(2, MAX_VERT + 1):
        for count in range(NUM_ITER):
            g, capacity = generate_random_graph(num_vertices)
            print(
                "Running benchmark on random graph with {:d} vertices and {:d} edges\n".format(
                    num_vertices,
                    g.num_edges()
                )
            )

            # Randomize source and target vertices
            v1 = random.randint(0, num_vertices - 1)
            v2 = random.randint(1, num_vertices - 1)
            if v2 == v1:
                v2 = v2 - 1

            print("Chose vertices {} and {}".format(v1, v2))

            results = goldberg.benchmark.benchmark_all(g, g.vertex(v1), g.vertex(v2), capacity)

            # Check that results are the same
            res = results[0][1]["maxflow"]
            for result in results:
                if result[1]["maxflow"] != res:
                    print("Error: computed max flows are different!")
                    exit(1)

            print("Writing results to random_graph_results.dat\n\n\n")
            f_res.write(
                "[{:d}, ".format(num_vertices)
                + "{:d}, ".format(g.num_edges())
                + json.dumps(results)
                + "]"
                + '\n'
            )

            print("Serializing graph in random_graph_results.dat\n\n\n")
            pickle.dump(g, f_graphs)

    print("Completed benchmarks on random graphs")

except KeyboardInterrupt:
    print("Benchmark interrupted")

finally:
    f_res.flush()
    f_res.close()
    f_graphs.flush()
    f_graphs.close()
