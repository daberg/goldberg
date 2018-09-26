import goldberg.algo
import graph_tool.generation

g = graph_tool.generation.complete_graph(60, directed=True)
capacity = g.new_edge_property("int")

for edge in g.edges():
    capacity[edge] = 5

goldberg.algo.stack_push_relabel(g, g.vertex(0), g.vertex(1), capacity)
