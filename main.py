import graph_tool


def debug(message):
    print("[Debug] " + message)
    pass


class FlowNetwork:
    def __init__(self, graph, capacity, source, sink):
        self.graph = graph
        self.capacity = capacity
        self.source = source
        self.sink = sink

        # Add reverse edge map
        self.reverse_edges = g.new_edge_property("object")
        edges = list(graph.edges())
        for edge in edges:
            new = graph.add_edge(edge.target(), edge.source())
            self.capacity[new] = 0
            self.reverse_edges[edge] = new
            self.reverse_edges[new] = edge

        # Add flow map
        self.flow = flow = graph.new_edge_property("double")

    def push_relabel(self):
        graph = self.graph
        capacity = self.capacity
        source = self.source
        sink = self.sink

        preflow = self.flow
        reverse_edges = self.reverse_edges

        # Create distance map
        distance = graph.new_vertex_property("int")

        # Create excess map
        excess = graph.new_vertex_property("double")

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

        cur_v = self._select_active(graph, excess)
        while cur_v:
            self._debug_print(distance, excess)

            # Look for admissible edges
            for out_e in cur_v.out_edges():

                # If admissible, push flow
                if (distance[cur_v] > distance[out_e.target()]
                    and capacity[out_e] - preflow[out_e] > 0):
                    debug("Selected admissible edge {}".format(out_e))

                    self._push(out_e, excess, capacity, preflow)

                    # Node not active anymore
                    if (excess[cur_v] <= 0):
                        break

            # No more admissible edges
            # Relabel if still active
            if (excess[cur_v] > 0):
                self._relabel(cur_v, distance, capacity, preflow)

            cur_v = self._select_active(graph, excess)

        self._debug_print(distance, excess)

        return excess[sink]

    def _push(self, edge, excess, capacity, preflow):
        origin = edge.source()
        dest = edge.target()

        delta = min(excess[origin], capacity[edge] - preflow[edge])

        preflow[edge] = preflow[edge] + delta
        rev = self.reverse_edges[edge]
        preflow[rev] = preflow[rev] - delta

        excess[origin] = excess[origin] - delta
        excess[dest] = excess[dest] + delta

        debug("Pushed {:f} from {} to {}".format(delta, origin, dest))

    def _relabel(self, vertex, distance, capacity, preflow):

        suitable_edges = list(filter(
            lambda edge : capacity[edge] - preflow[edge] > 0, vertex.out_edges()
        ))

        if not suitable_edges:
            # TODO why is this happening?
            debug("Could not relabel {}, no admissible arcs".format(vertex))
            return

        dists = map(
            lambda edge : distance[edge.target()], suitable_edges
        )

        new_d = min(dists) + 1

        distance[vertex] = new_d
        debug("Relabeled vertex {} with distance {:d}".format(vertex, new_d))

    def _select_active(self, graph, excess):
        for v in graph.vertices():
            if excess[v] > 0 and v != self.sink:
                debug("Selected node " + str(v))
                return v
        debug("Found no active nodes")
        return None

    def _debug_print(self, distance, excess):
        for e in self.graph.edges():
            debug("Edge {}:\tc={}\tf={}".format(e, self.capacity[e], self.flow[e]))
        debug("")
        for v in self.graph.vertices():
            debug("Vertex {}:\td={}\te={}".format(v, distance[v], excess[v]))


import graph_tool.flow

g = graph_tool.Graph(directed=True)

capacity = g.new_edge_property("double")
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

net = FlowNetwork(g, capacity, s, t)
print("Custom implementation detected flow: {}".format(net.push_relabel()))

res = graph_tool.flow.push_relabel_max_flow(g, s, t, g.ep.capacity)
res.a = g.ep.capacity.get_array() - res.get_array()
print("BGL implementation detected flow: {}".format(sum(res[e] for e in t.in_edges())))
