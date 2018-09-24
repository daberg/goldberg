import graph_tool


def debug(message):
    print("[Debug] " + message)

def push_relabel(graph, source, target, capacity):
    # Add residual edges and create reverse edge map
    reverse_edges = _create_residual_edges(graph, capacity)

    # Create preflow map
    preflow = graph.new_edge_property("int")

    # Create distance map
    distance = graph.new_vertex_property("int")

    # Create excess map
    excess = graph.new_vertex_property("int")

    # Initializing distance and excess
    for v in graph.vertices():
        distance[v] = 0
        excess[v] = 0
    distance[source] = graph.num_vertices()

    # Initializing preflow
    for edge in graph.edges():
        preflow[edge] = 0

    # Saturate edges outgoing from source
    for s_out in source.out_edges():
        cap = capacity[s_out]

        # If capacity is 0, nothing to push
        # Probably an added residual arc
        # Skip cycle just for optimization
        if cap == 0:
            continue

        preflow[s_out] = cap
        preflow[reverse_edges[s_out]] = - cap

        excess[s_out.target()] = excess[s_out.target()] + cap
        excess[source] = excess[source] - cap

        debug("Saturated edge {}".format(s_out))

    debug("Initialized")

    cur_v = _select_active(graph, excess, target)
    while cur_v:
        _debug_print(graph, capacity, preflow, distance, excess)

        # Look for admissible edges
        for out_e in cur_v.out_edges():

            # If admissible, push flow
            if (distance[cur_v] > distance[out_e.target()]
                and capacity[out_e] - preflow[out_e] > 0):
                debug("Selected admissible edge {}".format(out_e))

                _push(out_e, excess, capacity, preflow, reverse_edges)

                # Node not active anymore
                if (excess[cur_v] <= 0):
                    break

        # No more admissible edges
        # Relabel if still active
        if (excess[cur_v] > 0):
            _relabel(cur_v, distance, capacity, preflow)

        cur_v = _select_active(graph, excess, target)

    debug("Reached optimal state")
    _debug_print(graph, capacity, preflow, distance, excess)

    return excess[target]

def _create_residual_edges(graph, capacity):
    reverse_edges = graph.new_edge_property("object")

    debug("Adding residual edges")

    newlist = []
    for edge in graph.edges():
        newlist.append((edge, edge.target(), edge.source()))

    for entry in newlist:
        debug("Adding residual edge from {} to {}".format(entry[1], entry[2]))
        new = graph.add_edge(entry[1], entry[2])
        capacity[new] = 0
        reverse_edges[entry[0]] = new
        reverse_edges[new] = edge

    return reverse_edges

def _push(edge, excess, capacity, preflow, reverse_edges):
    origin = edge.source()
    dest = edge.target()

    delta = min(excess[origin], capacity[edge] - preflow[edge])

    preflow[edge] = preflow[edge] + delta
    rev = reverse_edges[edge]
    preflow[rev] = preflow[rev] - delta

    excess[origin] = excess[origin] - delta
    excess[dest] = excess[dest] + delta

    debug("Pushed {:f} from {} to {}".format(delta, origin, dest))

def _relabel(vertex, distance, capacity, preflow):
    # There must be at least a suitable edge
    suitable_edges = filter(
        lambda edge : capacity[edge] - preflow[edge] > 0, vertex.out_edges()
    )

    dists = map(
        lambda edge : distance[edge.target()], suitable_edges
    )

    new_d = min(dists) + 1

    distance[vertex] = new_d
    debug("Relabeled vertex {} with distance {:d}".format(vertex, new_d))

def _select_active(graph, excess, sink):
    for v in graph.vertices():
        if excess[v] > 0 and v != sink:
            debug("Selected node " + str(v))
            return v
    debug("Found no active nodes")
    return None

def _debug_print(graph, capacity, preflow, distance, excess):
    for e in graph.edges():
        debug("Edge {}:\tc={}\tf={}".format(e, capacity[e], preflow[e]))
    debug("")
    for v in graph.vertices():
        debug("Vertex {}:\td={}\te={}".format(v, distance[v], excess[v]))


def test_implementations(graph, source, target, capacity):
    import graph_tool.flow
    import time

    print("Running max flow implementation benchmark")
    print()
    print("Number of vertices:   {}".format(graph.num_vertices()))
    print("Number of edges:      {}".format(graph.num_edges()))
    print()

    start = time.time()
    maxflow = push_relabel(graph, source, target, capacity)
    end = time.time()

    print("Custom implementation detected flow: {}".format(maxflow))
    print("Elapsed time: {} ms".format((end - start) * 1000.0))
    print()

    start = time.time()
    res = graph_tool.flow.push_relabel_max_flow(graph, source, target, capacity)
    end = time.time()

    res.a = capacity.get_array() - res.get_array()
    print("BGL implementation detected flow: {}".format(sum(res[e] for e in target.in_edges())))
    print("Elapsed time: {} ms".format((end - start) * 1000.0))
    print()


g = graph_tool.Graph(directed=True)

capacity = g.new_edge_property("int")
g.ep.capacity = capacity

s = g.add_vertex()
u = g.add_vertex()
v = g.add_vertex()
t = g.add_vertex()

e_su = g.add_edge(s, u)
e_ut = g.add_edge(u, t)
e_sv = g.add_edge(s, v)
e_vt = g.add_edge(v, t)

e_us = g.add_edge(u, s)

g.ep.capacity[e_su] = 5
g.ep.capacity[e_ut] = 4
g.ep.capacity[e_sv] = 6
g.ep.capacity[e_vt] = 5

g.ep.capacity[e_us] = 3

import graph_tool.generation
import random

#g = graph_tool.generation.random_graph(500, lambda: (random.randint(2, 10), random.randint(2, 10)))
#capacity = g.new_edge_property("double")
#for edge in g.edges():
#    capacity[edge] = random.randint(1, 10)
#test_implementations(g, g.vertex(0), g.vertex(1), capacity)

g = graph_tool.generation.complete_graph(20, directed=True)
capacity = g.new_edge_property("int")
for edge in g.edges():
    capacity[edge] = 5
test_implementations(g, g.vertex(0), g.vertex(1), capacity)

#g = graph_tool.generation.lattice([5, 5])
#g.set_directed(True)
#capacity = g.new_edge_property("int")
#for edge in g.edges():
#    capacity[edge] = random.randint(1, 10)
#test_implementations(g, g.vertex(0), g.vertex(1), capacity)
