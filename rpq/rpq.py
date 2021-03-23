#!/usr/bin/env python3

from .ordered_multiset import OrderedMultiset
from .zero_prefix_bst import ZeroPrefixBST
from .max_bst import MaxBST
from .min_bst import MinBST

class RetroactivePriorityQueue:
    """A partially retroactive priority queue.

    A priority queue can be represented as a sequence of *insert* and
    *delete-min* operations, each with a unique *time*. This data structure
    efficently supports:
        - Adding or removing an operation at a given time.
        - Observing the contents of the queue after all operations have been
          applied (using the standard Collection interface).

    The times of all operations must be totally ordered and the values
    inserted in the queue must be partially ordered.
    """

    def __init__(self):
        """Initialize a queue with no operations."""
        self._q_now = OrderedMultiset()
        self._inserts_in_q = MinBST()
        self._deleted_inserts = MaxBST()
        self._bridges = ZeroPrefixBST()
        self._size_changes = ZeroPrefixBST()

    def _insert_for_t(self, t):
        bridge = self._bridges.zero_prefix_before(t)
        insert_v, insert_t = self._deleted_inserts.agg_after(
            bridge, include_eq=True
        )
        return insert_t, insert_v

    def _delete_for_t(self, t):
        bridge = self._bridges.zero_prefix_after(t)
        delete_v, delete_t = self._inserts_in_q.agg_before(
            bridge, include_eq=True
        )
        return delete_t, delete_v

    def _promote_to_q(self, t, v):
        self._q_now.add(v)
        self._inserts_in_q[t] = v
        self._deleted_inserts.remove(t)
        self._bridges[t] = 0

    def _delete_from_q(self, t, v):
        self._q_now.remove(v)
        self._inserts_in_q.remove(t)
        self._deleted_inserts[t] = v
        self._bridges[t] = 1

    def _is_empty_after(self, t):
        agg_before = self._size_changes.agg_before(t, include_eq = True)
        if agg_before is None or agg_before.sum == 0:
            return True

        agg = self._size_changes.agg()
        if agg.min_prefix_sum == 0 and agg.min_prefix_last_key >= t:
            return True
        else:
            return False

    def add_insert(self, t, value):
        """Create a new insert operation

        Args:
            t: The time at which the insertion is performed.
            value: The value to be inserted at time t.

        Raises:
            KeyError: If the queue already contains an operation with time t.
        """
        if t in self._bridges:
            raise KeyError

        # Insert as if it is be deleted
        self._deleted_inserts[t] = value
        self._bridges[t] = 1
        self._size_changes[t] = 1

        insert_t, insert_v = self._insert_for_t(t)
        self._promote_to_q(insert_t, insert_v)

    def _remove_delete_min(self, t):
        insert_t, insert_v = self._insert_for_t(t)

        self._bridges.remove(t)
        self._size_changes.remove(t)

        self._promote_to_q(insert_t, insert_v)


    def add_delete_min(self, t):
        """Create a new delete-min operation

        Args:
            t: The time at which the delete-min is performed.

        Raises:
            KeyError: If the queue already contains an operation with time t.
            ValueError: If performing a delete-min at time t would lead to a
                delete-min on an empty queue at some time t* >= t.
        """
        if t in self._bridges:
            raise KeyError
        if self._is_empty_after(t):
            raise ValueError

        delete_t, delete_v = self._delete_for_t(t)

        self._bridges[t] = -1
        self._size_changes[t] = -1

        self._delete_from_q(delete_t, delete_v)

    def _remove_insert_in_q(self, t):
        v = self._inserts_in_q[t]

        self._q_now.remove(v)
        self._inserts_in_q.remove(t)
        self._bridges.remove(t)
        self._size_changes.remove(t)

    def _remove_deleted_insert(self, t):
        delete_t, delete_v = self._delete_for_t(t)
        self._delete_from_q(delete_t, delete_v)

        self._deleted_inserts.remove(t)
        self._bridges.remove(t)
        self._size_changes.remove(t)


    def remove(self, t):
        """Remove an operation

        Args:
            t: The time of the operation to be removed.

        Raises:
            KeyError: If the queue does not contain an operation with time t.
            ValueError: If the operation at time t is an insertion and removing
                it would lead to a delete-min on an empty queue at some time
                t* > t.
        """

        if t not in self._bridges:
            raise KeyError

        op_type = self._bridges[t]

        if op_type < 0:
            self._remove_delete_min(t)
        elif op_type == 0:
            self._remove_insert_in_q(t)
        else:
            if self._is_empty_after(t):
                raise ValueError
            self._remove_deleted_insert(t)

    def __iter__(self):
        """
        Yields:
            The values in the queue after all operations are performed.
        """
        yield from self._q_now

    def __len__(self):
        """
        Returns:
            The size of the queue after all operations are performed.
        """
        return len(self._q_now)

    def __contains__(self, v):
        """
        Returns:
            Whether the queue contains v after all operations are performed.
        """
        return v in self._q_now
