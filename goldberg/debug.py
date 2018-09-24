import os


def info(message):
    _print_functions["info"](message)

def error(message):
    _print_functions["error"](message)

def _dummy(message):
    pass

def _info(message):
    print("[Info] " + message)

def _error(message):
    print("[Error] " + message)


_print_functions = {
    "info" : _info if "GOLDBERGDEBUG" in os.environ else _dummy,
    "error" : _error
}
