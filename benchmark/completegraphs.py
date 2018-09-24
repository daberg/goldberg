import goldberg.benchmark
import graph_tool.generation


g = graph_tool.generation.complete_graph(20, directed=True)
capacity = g.new_edge_property("int")
for edge in g.edges():
    capacity[edge] = 5
goldberg.benchmark.benchmark_all(g, g.vertex(0), g.vertex(1), capacity)
