import graph_tool.flow
import time
import goldberg.algo


def benchmark_all(graph, source, target, capacity):

    results = []

    _print_separator()
    print("Number of vertices:       {}".format(graph.num_vertices()))
    print("Number of edges:          {}".format(graph.num_edges()))
    _print_separator()

    # BGL implementation
    ret = profilerun(
        "BGL implementation",
        graph_tool.flow.push_relabel_max_flow,
        graph, source, target, capacity
    )

    residual_capacity = ret[0]
    residual_capacity.a = capacity.get_array() - residual_capacity.get_array()
    maxflow = sum(residual_capacity[e] for e in target.in_edges())

    result = _compose_result(maxflow, ret[1], ret[2])
    results.append(result)

    _print_result(result)
    _print_separator()

    # Custom push-relabel implementation
    ret = profilerun(
        "custom push-relabel implementation",
        goldberg.algo.push_relabel,
        graph, source, target, capacity
    )

    flow = ret[0]
    maxflow = sum(flow[e] for e in target.in_edges())

    result = _compose_result(maxflow, ret[1], ret[2])
    results.append(result)

    _print_result(result)
    _print_separator()

def profilerun(name, func, graph, source, target, capacity):
    print("Profiling {:s}...".format(name))

    start_time = time.time()
    ret = func(graph, source, target, capacity)
    end_time = time.time()

    memory = 0

    return (ret, (end_time - start_time) * 1000.0, memory)

def _compose_result(maxflow, time, memory):
    result = {
        "maxflow" : maxflow,
        "time" : time,
        "memory" : memory
    }
    return result

def _print_result(result):
    print("Computed maximum flow:    {}".format(result["maxflow"]))
    print("Elapsed time:             {} ms".format(result["time"]))
    print("Allocated memory:         {}".format(result["memory"]))

def _print_separator():
    print(separator)


separator = "-" * 79
