import goldberg.debug as debug


def check_parameters(graph, source, target, capacity):
    if not graph.is_directed():
        debug.error("Graph not directed")
        raise ValueError()

    if capacity.get_graph() is not graph:
        debug.error("Capacity map does not refer to graph")
        raise ValueError()

    if capacity.value_type()[:3] != "int":
        debug.error("Capacity map type is {} instead of an integer type".format(capacity.value_type()))
        raise ValueError()

def create_maps(graph, capacity):
    # Add residual edges and create reverse edge map
    reverse_edges = _create_residual_edges(graph, capacity)

    # Create preflow map
    preflow = graph.new_edge_property("int")

    # Create distance map
    distance = graph.new_vertex_property("int")

    # Create excess map
    excess = graph.new_vertex_property("int")

    return reverse_edges, preflow, distance, excess

def push(edge, excess, capacity, preflow, reverse_edges):
    origin = edge.source()
    dest = edge.target()

    delta = min(excess[origin], capacity[edge] - preflow[edge])

    preflow[edge] = preflow[edge] + delta
    rev = reverse_edges[edge]
    preflow[rev] = preflow[rev] - delta

    excess[origin] = excess[origin] - delta
    excess[dest] = excess[dest] + delta

    debug.info("Pushed {:f} from {} to {}".format(delta, origin, dest))

def relabel(vertex, distance, capacity, preflow):
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

def select_active(graph, excess, sink):
    for v in graph.vertices():
        if excess[v] > 0 and v != sink:
            debug.info("Selected node " + str(v))
            return v
    debug.info("Found no active nodes")
    return None

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
