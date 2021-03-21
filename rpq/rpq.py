#!/usr/bin/env python3

from .ordered_multiset import OrderedMultiset
from .zero_prefix_bst import ZeroPrefixBST
from .max_bst import MaxBST
from .min_bst import MinBST

class RetroactivePriorityQueue:
    # Assumes that all keys are unique

    def __init__(self):
        self.q_now = OrderedMultiset()
        self.inserts_in_q = MinBST()
        self.deleted_inserts = MaxBST()
        self.bridges = ZeroPrefixBST()
        self.size_changes = ZeroPrefixBST()

    def add_insert(self, t, value):
        if t in self.bridges:
            raise KeyError

        # Insert as if it is be deleted
        self.deleted_inserts[t] = value
        self.bridges[t] = 1
        self.size_changes[t] = 1

        # Find the value to insert in q_now
        bridge = self.bridges.zero_prefix_before(t)
        insert_v, insert_t = self.deleted_inserts.agg_after(
            bridge, include_eq=True
        )

        # Update BSTs
        self.q_now.add(insert_v)
        self.inserts_in_q[insert_t] = insert_v
        self.deleted_inserts.remove(insert_t)
        self.bridges[insert_t] = 0

    def _remove_delete_min(self, t):
        # Find the value to insert in q_now
        bridge = self.bridges.zero_prefix_before(t)
        insert_v, insert_t = self.deleted_inserts.agg_after(
            bridge, include_eq=True
        )

        # Update BSTs
        self.bridges.remove(t)
        self.size_changes.remove(t)

        self.q_now.add(insert_v)
        self.inserts_in_q[insert_t] = insert_v
        self.deleted_inserts.remove(insert_t)
        self.bridges[insert_t] = 0


    def _is_empty_after(self, t):
        agg_before = self.size_changes.agg_before(t, include_eq = True)
        if agg_before is None or agg_before.sum == 0:
            return True

        agg = self.size_changes.agg()
        if agg.min_prefix_sum == 0 and agg.min_prefix_last_key >= t:
            return True
        else:
            return False

    def add_delete_min(self, t):
        if t in self.bridges:
            raise KeyError
        if self._is_empty_after(t):
            raise ValueError

        bridge = self.bridges.zero_prefix_after(t)
        delete_v, delete_t = self.inserts_in_q.agg_before(
            bridge, include_eq=True
        )

        self.bridges[t] = -1
        self.size_changes[t] = -1

        self.q_now.remove(delete_v)
        self.inserts_in_q.remove(delete_t)
        self.deleted_inserts[delete_t] = delete_v
        self.bridges[delete_t] = 1

    def _remove_insert_in_q(self, t):
        v = self.inserts_in_q[t]

        self.q_now.remove(v)
        self.inserts_in_q.remove(t)
        self.bridges.remove(t)
        self.size_changes.remove(t)

    def _remove_deleted_insert(self, t):
        bridge = self.bridges.zero_prefix_after(t)
        delete_v, delete_t = self.inserts_in_q.agg_before(
            bridge, include_eq=True
        )

        self.q_now.remove(delete_v)
        self.inserts_in_q.remove(delete_t)
        self.deleted_inserts[delete_t] = delete_v
        self.bridges[delete_t] = 1

        self.deleted_inserts.remove(t)
        self.bridges.remove(t)
        self.size_changes.remove(t)


    def remove(self, t):
        if t not in self.bridges:
            raise KeyError

        op_type = self.bridges[t]

        if op_type < 0:
            self._remove_delete_min(t)
        elif op_type == 0:
            self._remove_insert_in_q(t)
        else:
            if self._is_empty_after(t):
                raise ValueError
            self._remove_deleted_insert(t)

    def __iter__(self):
        yield from self.q_now
