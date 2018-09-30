class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

    def __str__(self):
        return str(self.data)

class Stack:
    def __init__(self):
        self.head = None

    def __str__(self):
        if not self.head:
            return "empty"

        ret = str(self.head)
        cur = self.head
        while cur.next:
            ret = ret + " " + str(cur.next)
            cur = cur.next

        return ret

    def push(self, data):
        new = Node(data)
        new.next = self.head
        self.head = new

    def pop(self):
        if self.head is None:
            return None
        else:
            tmp = self.head
            self.head = self.head.next
            return tmp.data
