import os


def info_algo(graph, capacity, preflow, distance, excess):
    _print_functions["info_algo"](graph, capacity, preflow, distance, excess)

def info(message):
    _print_functions["info"](message)

def error(message):
    _print_functions["error"](message)

def _info_algo(graph, capacity, preflow, distance, excess):
    for e in graph.edges():
        info("Edge {}:\tc={}\tf={}".format(e, capacity[e], preflow[e]))
    info("")
    for v in graph.vertices():
        info("Vertex {}:\td={}\te={}".format(v, distance[v], excess[v]))

def _dummy(*arg):
    pass

def _info(message):
    print("[Info] " + message)

def _error(message):
    print("[Error] " + message)


debug_mode = True if "GOLDBERGDEBUG" in os.environ else False

_print_functions = {
    "info_algo" : _info_algo if debug_mode else _dummy,
    "info" : _info if debug_mode else _dummy,
    "error" : _error
}
