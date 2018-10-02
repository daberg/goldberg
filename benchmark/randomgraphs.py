import goldberg.benchmark
import graph_tool.generation
import graph_tool.topology
import json
import pickle
import random


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


f_res = open('benchmark/results/random_graph_results.dat', "w")
f_graphs = open('benchmark/results/random_graphs.dat', "wb")

try:
    for num_vertices in range(2, 100):
        for count in range(25):
            g, capacity = generate_random_graph(num_vertices)
            print(
                "Running benchmark on random graph with {:d} vertices and {:d} edges\n".format(
                    num_vertices,
                    g.num_edges()
                )
            )
            for v in g.vertices():
                print(v)
            for edge in g.edges():
                print("Edge {}: c={}".format(edge, capacity[edge]))

            # Randomize source and target vertices
            # Pick a reasonably long path between them
            while True:
                v1 = random.randint(0, num_vertices - 1)
                v2 = random.randint(1, num_vertices - 1)
                if v2 == v1:
                    v2 = v2 - 1

                print("Chose vertices {} and {}".format(v1, v2))

                paths_iter = graph_tool.topology.all_paths(
                    g,
                    v1,
                    v2,
                    max(2, num_vertices / 2)
                )

                try:
                    path = max(paths_iter, key=len)
                    break
                except ValueError:
                    print("No path exists between selected vertices")
                    print("Starting again")

            print("Found a path of length {:d} between selected vertices".format(len(path)))

            results = goldberg.benchmark.benchmark_all(g, g.vertex(path[0]), g.vertex(path[-1]), capacity)

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
                + json.dumps(results) + ", {:d}]".format(len(path))
                + '\n'
            )

            print("Serializing graph in random_graph_results.dat\n\n\n")
            pickle.dump(g, f_graphs)

except KeyboardInterrupt:
    print("Interrupted")

finally:
    f_res.flush()
    f_res.close()
    f_graphs.flush()
    f_graphs.close()

print("Completed benchmarks on random graphs")
