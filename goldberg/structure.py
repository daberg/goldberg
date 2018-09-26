import collections


class Stack:
    def __init__(self):
        self._repr = collections.deque()

    def push(self, element):
        self._repr.append(element)

    def pop(self):
        try:
            return self._repr.pop()
        except IndexError:
            return None
