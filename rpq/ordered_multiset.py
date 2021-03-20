from .treap import Treap

class OrderedMultiset():
    def __init__(self):
        self.treap = Treap(lambda x, y: None)

    def add(self, value):
        prev_cnt = 0
        try:
            prev_cnt = self.treap[value]
        except KeyError:
            pass
        self.treap[value] = prev_cnt + 1

    def __in__(self, value):
        return value in self.treap

    def __iter__(self):
        for v, cnt in self.treap:
            for _ in range(cnt):
                yield v

    def remove(self, value):
        prev_cnt = self.treap[value]
        if prev_cnt == 1:
            self.treap.remove(value)
        else:
            self.treap[value] = prev_cnt - 1
