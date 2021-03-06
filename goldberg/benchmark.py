import goldberg.algo as algo
import graph_tool.flow
import time
import memory_profiler


def benchmark_all(graph, source, target, capacity):

    graph.edge_properties["capacity"] = capacity
    original_g = graph

    results = []

    print("Running benchmarks for all implementations")
    _print_separator()
    print("Input stats")
    print()
    print("Number of vertices:       {}".format(graph.num_vertices()))
    print("Number of edges:          {}".format(graph.num_edges()))
    _print_separator()

    # BGL implementation
    name="BGL implementation"

    graph = original_g.copy()
    capacity = graph.edge_properties["capacity"]

    residual_capacity, time, mem = profilerun(
        graph_tool.flow.push_relabel_max_flow,
        graph,
        graph.vertex(original_g.vertex_index[source]),
        graph.vertex(original_g.vertex_index[target]),
        capacity
    )

    residual_capacity.a = capacity.get_array() - residual_capacity.get_array()
    maxflow = sum(residual_capacity[e] for e in target.in_edges())

    result = _compose_result(maxflow, time, mem)
    results.append((name, result))

    print("{} run stats".format(name))
    print()
    _print_result(result)
    _print_separator()

    # Stack push-relabel implementation
    name="Stack push-relabel"

    graph = original_g.copy()
    capacity = graph.edge_properties["capacity"]

    flow, time, mem = profilerun(
        algo.stack_push_relabel,
        graph,
        graph.vertex(original_g.vertex_index[source]),
        graph.vertex(original_g.vertex_index[target]),
        capacity
    )

    maxflow = sum(flow[e] for e in target.in_edges())

    result = _compose_result(maxflow, time, mem)
    results.append((name, result))

    print("{} run stats".format(name))
    print()
    _print_result(result)
    _print_separator()

    return results

def profilerun(flownet_function, graph, source, target, capacity):
    start_time = time.time()
    ret = flownet_function(graph, source, target, capacity)
    end_time = time.time()

    time_diff = end_time - start_time

    interval = time_diff / 1000.0
    start_mem = memory_profiler.memory_usage(lambda: None, max_usage=True)[0]
    end_mem = memory_profiler.memory_usage(
        (flownet_function, [graph, source, target, capacity]),
        interval=interval,
        timeout=time_diff,
        max_usage=True
    )[0]

    mem_diff = end_mem - start_mem

    return (ret, time_diff * 1000.0, mem_diff * 1024.0)

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
    print("Allocated memory:         {} KiB".format(result["memory"]))

def _print_separator():
    print(separator)


separator = "-" * 79
