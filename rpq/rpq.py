#!/usr/bin/env python3

from .ordered_multiset import OrderedMultiset
from .bridge_bst import BridgeBST
from .max_bst import MaxBST
from .min_bst import MinBST

class RetroactivePriorityQueue:
    # Assumes that all keys are unique

    def __init__(self):
        self.q_now = OrderedMultiset()
        self.inserts_in_q = MinBST()
        self.deleted_inserts = MaxBST()
        self.bridges = BridgeBST()

    def _core_add_insert(self, t):
        bridge = self.bridges.bridge_before(t)

        insert_v, insert_t = self.deleted_inserts.agg_after(
            bridge, include_eq=True
        )

        self.q_now.add(insert_v)
        self.inserts_in_q[insert_t] = insert_v
        self.deleted_inserts.remove(insert_t)
        self.bridges[insert_t] = 0

    def add_insert(self, t, value):
        if t in self.bridges:
            raise KeyError

        self.deleted_inserts[t] = value
        self.bridges[t] = 1
        self._core_add_insert(t)


    def _core_add_delete(self, t):
        bridge = self.bridges.bridge_after(t)

        delete_v, delete_t = self.inserts_in_q.agg_before(
            bridge, include_eq=True
        )

        self.q_now.remove(delete_v)
        self.inserts_in_q.remove(delete_t)
        self.deleted_inserts[delete_t] = delete_v
        self.bridges[delete_t] = 1

    def add_delete_min(self, t):
        if t in self.bridges:
            raise KeyError
        if self.inserts_in_q.agg_before(t) is None:
            raise ValueError

        self._core_add_delete(t)
        self.bridges[t] = -1

    def remove(self, t):
        if t not in self.bridges:
            raise KeyError

        if self.bridges[t] < 0:
            # remove delete_min
            self._core_add_insert(t)
        else:
            # remove insert
            self._core_add_delete(t)
            self.deleted_inserts.remove(t)

        self.bridges.remove(t)

    def min(self):
        return next(iter(self), None)

    def __iter__(self):
        yield from self.q_now

def test_priority_queue():
    queue = RetroactivePriorityQueue()
    assert list(queue) == []

    queue.add_insert(0, 5)
    assert list(queue) == [5]
    queue.add_insert(10, 3)
    assert list(queue) == [3, 5]
    queue.add_delete_min(5)
    assert list(queue) == [3]
    queue.add_insert(2, 7)
    assert list(queue) == [3, 7]
    queue.add_insert(3, 4)
    assert list(queue) == [3, 5, 7]
    queue.add_delete_min(7)
    assert list(queue) == [3, 7]

    # delete insert
    queue.remove(2)
    assert list(queue) == [3]

    # delete delete
    queue.remove(5)
    assert list(queue) == [3, 5]


    print("test_priority_queue() passed")

if __name__ == "__main__":
    test_priority_queue()
