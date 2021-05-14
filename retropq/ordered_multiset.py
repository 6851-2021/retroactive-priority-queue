from .treap import Treap

class OrderedMultiset():
    def __init__(self):
        self._treap = Treap(lambda x, y: None)
        self._len = 0

    def add(self, value):
        prev_cnt = 0
        try:
            prev_cnt = self._treap[value]
        except KeyError:
            pass
        self._treap[value] = prev_cnt + 1

        self._len += 1

    def remove(self, value):
        prev_cnt = self._treap[value]
        if prev_cnt == 1:
            self._treap.remove(value)
        else:
            self._treap[value] = prev_cnt - 1

        self._len -= 1

    def __in__(self, value):
        return value in self._treap

    def __iter__(self):
        for v, cnt in self._treap:
            for _ in range(cnt):
                yield v

    def __len__(self):
        return self._len
