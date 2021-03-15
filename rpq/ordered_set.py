from .treap import Treap

class OrderedSet():
    def __init__(self):
        self.treap = Treap(lambda x, y: None)

    def add(self, value):
        self.treap[value] = True

    def __in__(self, value):
        return value in self.treap

    def __iter__(self):
        for k, _ in self.treap:
            yield k

    def remove(self, value):
        self.treap.remove(value)
