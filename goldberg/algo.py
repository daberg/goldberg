import goldberg.debug as debug
import goldberg.helper as helper
import goldberg.structure as structure


def naive_push_relabel(graph, source, target, capacity):
    # Initializing data maps
    reverse_edges, preflow, distance, excess = helper.create_maps(graph, capacity)

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

    cur_v = helper.select_active(graph, excess, target)
    while cur_v:
        debug.debug_print(graph, capacity, preflow, distance, excess)

        # Look for admissible edges
        for out_e in cur_v.out_edges():

            # If admissible, push flow
            if (distance[cur_v] > distance[out_e.target()]
                and capacity[out_e] - preflow[out_e] > 0):
                debug.info("Selected admissible edge {}".format(out_e))

                helper.push(out_e, excess, capacity, preflow, reverse_edges)

                # Node not active anymore
                if (excess[cur_v] <= 0):
                    break

        # No more admissible edges
        # Relabel if still active
        if (excess[cur_v] > 0):
            helper.relabel(cur_v, distance, capacity, preflow)

        cur_v = helper.select_active(graph, excess, target)

    debug.info("Reached optimal state")
    debug.debug_print(graph, capacity, preflow, distance, excess)

    return preflow

def stack_push_relabel(graph, source, target, capacity):
    # Initializing data maps
    reverse_edges, preflow, distance, excess = helper.create_maps(graph, capacity)

    # Initializing stack to keep active node
    actives = structure.Stack()

    # Initializing active map
    is_active = graph.new_vertex_property("bool")

    # Initializing distance, excess and active property
    for v in graph.vertices():
        distance[v] = 0
        excess[v] = 0
        is_active[v] = False
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

        # Since node has become active, add it to active stack
        active = s_out.target()
        if active != target and is_active[active] == False:
            actives.push(active)
            is_active[active] = True

        debug.info("Saturated edge {}".format(s_out))

    debug.info("Initialized")

    cur_v = actives.pop()
    while cur_v:
        debug.debug_print(graph, capacity, preflow, distance, excess)

        # Look for admissible edges
        for out_e in cur_v.out_edges():

            # If admissible, push flow
            if (distance[cur_v] > distance[out_e.target()]
                and capacity[out_e] - preflow[out_e] > 0):
                debug.info("Selected admissible edge {}".format(out_e))

                helper.push(out_e, excess, capacity, preflow, reverse_edges)

                active = out_e.target()
                if active != target and is_active[active] == False:
                    actives.push(active)
                    is_active[active] = True

                # Node not active anymore
                if (excess[cur_v] <= 0):
                    is_active[active] = False
                    break

        # No more admissible edges
        # Relabel if still active
        if (excess[cur_v] > 0):
            helper.relabel(cur_v, distance, capacity, preflow)
            actives.push(cur_v)

        cur_v = actives.pop()

    debug.info("Reached optimal state")
    debug.debug_print(graph, capacity, preflow, distance, excess)

    return preflow
