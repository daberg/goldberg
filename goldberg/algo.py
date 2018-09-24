import graph_tool
import goldberg.debug as debug


def push_relabel(graph, source, target, capacity):
    # Perform sanity checks
    if not graph.is_directed():
        debug.error("Graph not directed")
        raise ValueError()

    if capacity.get_graph() is not graph:
        debug.error("Capacity map does not refer to graph")
        raise ValueError()

    if capacity.value_type()[:3] != "int":
        debug.error("Capacity map type is {} instead of an integer type".format(capacity.value_type()))
        raise ValueError()

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

        debug.info("Saturated edge {}".format(s_out))

    debug.info("Initialized")

    cur_v = _select_active(graph, excess, target)
    while cur_v:
        _debug_print(graph, capacity, preflow, distance, excess)

        # Look for admissible edges
        for out_e in cur_v.out_edges():

            # If admissible, push flow
            if (distance[cur_v] > distance[out_e.target()]
                and capacity[out_e] - preflow[out_e] > 0):
                debug.info("Selected admissible edge {}".format(out_e))

                _push(out_e, excess, capacity, preflow, reverse_edges)

                # Node not active anymore
                if (excess[cur_v] <= 0):
                    break

        # No more admissible edges
        # Relabel if still active
        if (excess[cur_v] > 0):
            _relabel(cur_v, distance, capacity, preflow)

        cur_v = _select_active(graph, excess, target)

    debug.info("Reached optimal state")
    _debug_print(graph, capacity, preflow, distance, excess)

    return preflow

def _create_residual_edges(graph, capacity):
    reverse_edges = graph.new_edge_property("object")

    debug.info("Adding residual edges")

    newlist = []
    for edge in graph.edges():
        newlist.append((edge, edge.target(), edge.source()))

    for entry in newlist:
        debug.info("Adding residual edge from {} to {}".format(entry[1], entry[2]))
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

    debug.info("Pushed {:f} from {} to {}".format(delta, origin, dest))

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
    debug.info("Relabeled vertex {} with distance {:d}".format(vertex, new_d))

def _select_active(graph, excess, sink):
    for v in graph.vertices():
        if excess[v] > 0 and v != sink:
            debug.info("Selected node " + str(v))
            return v
    debug.info("Found no active nodes")
    return None

def _debug_print(graph, capacity, preflow, distance, excess):
    for e in graph.edges():
        debug.info("Edge {}:\tc={}\tf={}".format(e, capacity[e], preflow[e]))
    debug.info("")
    for v in graph.vertices():
        debug.info("Vertex {}:\td={}\te={}".format(v, distance[v], excess[v]))
