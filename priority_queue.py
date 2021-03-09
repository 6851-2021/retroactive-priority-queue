#!/usr/bin/env python3

import collections
import heapq


# all t unique integers; all k unique integers
Insertion = collections.namedtuple("Insertion", ["t", "k"])
Deletion = collections.namedtuple("Deletion", "t")


class InsertionBST:  # unbalanced
    def __init__(self, data=None):
        self.data = data
        # assume when inserting that it is later deleted
        self.max_deleted = None if data is None else data
        self.left = None
        self.right = None
    
    def insert(self, data):
        if not self.data:
            self.__init__(data)
        else:
            self.max_deleted = max(self.max_deleted, data, key=lambda insertion: insertion.k)
            if data < self.data:
                if not self.left:
                    self.left = InsertionBST(data)
                else:
                    self.left.insert(data)
            else:
                if not self.right:
                    self.right = InsertionBST(data)
                else:
                    self.right.insert(data)

    def update_added(self, data):
        if self.data == data:
            if not self.left:
                if not self.right:
                    self.max_deleted = Insertion(None, -float("inf"))
                else:
                    self.max_deleted = self.right.max_deleted
            elif not self.right:
                self.max_deleted = self.left.max_deleted
            else:
                self.max_deleted = max(
                    self.left.max_deleted, self.right.max_deleted, key=lambda insertion: insertion.k)
        else:
            if data < self.data:
                self.left.update_added(data)
            else:
                self.right.update_added(data)
            if self.max_deleted == data:
                self.max_deleted = Insertion(None, -float("inf"))
                if self.left:
                    self.max_deleted = self.left.max_deleted
                if self.right:
                    self.max_deleted = max(
                        self.max_deleted, self.right.max_deleted, key=lambda insertion: insertion.k)

    def max_deleted_after(self, t):
        """ get Insertion with max k deleted after time t """
        current = self
        suffix_max = Insertion(t+1, -float("inf"))
        while current is not None:
            if t < current.data.t:
                suffix_max = max(
                    suffix_max, current.data, key=lambda insertion: insertion.k)
                if current.right:
                    suffix_max = max(
                        suffix_max, current.right.max_deleted, key=lambda insertion: insertion.k)
                current = current.left
            elif t > current.data.t:
                current = current.right
            else:
                break
        return suffix_max

def test_insertion_bst():
    insertion_bst = InsertionBST()
    insertion_bst.insert(Insertion(1, 5))
    assert insertion_bst.max_deleted_after(0).k == 5
    insertion_bst.insert(Insertion(2, 6))
    insertion_bst.insert(Insertion(-1, 7))
    assert insertion_bst.max_deleted_after(0).k == 6
    assert insertion_bst.max_deleted_after(-3).k == 7
    insertion_bst.update_added(Insertion(2, 6))
    assert insertion_bst.max_deleted_after(0).k == 5
    print("test_insertion_bst() passed")

class UpdateBST:  # also not balanced
    def __init__(self, data=None):
        self.data = data
        self.net_inserts = 1 if type(data) == Insertion else -1  # starts off not in Qnow
        self.min_prefix_sum = self.net_inserts  # of 1 if insertion that is not in Qnow, -1 if deletion
        self.max_prefix_sum = self.net_inserts
        self.left = None
        self.right = None

    def _get_node_value(self):
        """ net_inserts if node had no children: returns -1, 0, or 1 """
        return self.net_inserts \
        - (self.left.net_inserts if self.left else 0) \
        - (self.right.net_inserts if self.right else 0) \

    def _update_prefix_sums(self):
        """ update min_prefix_sum and max_prefix_sum """
        self.min_prefix_sum = float("inf")
        self.max_prefix_sum = -float("inf")
        if self.left:
            self.min_prefix_sum = min(self.min_prefix_sum, self.left.min_prefix_sum)
            self.max_prefix_sum = max(self.max_prefix_sum, self.left.max_prefix_sum)
        left_prefix_sum = self.net_inserts - (self.right.net_inserts if self.right else 0)
        self.min_prefix_sum = min(self.min_prefix_sum, left_prefix_sum)
        self.max_prefix_sum = max(self.max_prefix_sum, left_prefix_sum)
        if self.right:
            self.min_prefix_sum = min(self.min_prefix_sum, left_prefix_sum + self.right.min_prefix_sum)
            self.max_prefix_sum = max(self.max_prefix_sum, left_prefix_sum + self.right.max_prefix_sum)

    def insert(self, data):
        if self.data is None:
            self.__init__(data)
        else:
            self.net_inserts += 1 if type(data) == Insertion else -1
            if data < self.data:
                if not self.left:
                    self.left = UpdateBST(data)
                else:
                    self.left.insert(data)
            else:
                if not self.right:
                    self.right = UpdateBST(data)
                else:
                    self.right.insert(data)
            self._update_prefix_sums()

    def update_added(self, data):
        """ show that data was added to Qnow """
        self.net_inserts -= 1
        if data < self.data:
            self.left.update_added(data)
        elif data > self.data:
            self.right.update_added(data)
        self._update_prefix_sums()

    def find_most_recent_bridge(self, t):  # returns some integer + 1/2
        current = self
        prefix_sum = 0
        path = []
        prefix_sums = []  # prefix does not include own entry
        # go down tree to t
        while current:
            path.append(current)
            prefix_sum += current.left.net_inserts if current.left else 0
            prefix_sums.append(prefix_sum)
            if t < self.data.t and current.left:
                current = current.left
                prefix_sum -= current.net_inserts
            elif t > self.data.t:
                prefix_sum += current._get_node_value()
                current = current.right
            else:
                break
        current = path.pop()
        prefix_sum = prefix_sums.pop()
        if current.data.t >= t and prefix_sum == 0:
            # reached successor of t
            return t - 0.5
        elif current.data.t < t:
            # reached predecessor of t
            if prefix_sum == 0:
                return current.data.t - 0.5
            elif prefix_sum + current._get_node_value() == 0:
                return t - 0.5
        # go back up to find appropriate subtree
        while path:
            current = path.pop()
            prefix_sum = prefix_sums.pop()
            if current.data.t <= t:
                if prefix_sum == 0:
                    return current.data.t - 0.5
                if current.left:
                    prefix_before_left_subtree = prefix_sum - current.left.net_inserts
                    if prefix_before_left_subtree + current.left.min_prefix_sum <= 0 \
                        <= prefix_sum + current.left.max_prefix_sum:
                        current = current.left
                        # prefix_before_subtree = prefix_before_left_subtree
                        prefix_sum = prefix_before_left_subtree
                        break
        # bridge exists within subtree
        while current:
            prefix_sum += current.left.net_inserts if current.left else 0
            if prefix_sum == 0:
                return current.data.t - 0.5
            if current.right:
                prefix_before_right_subtree = prefix_sum + current._get_node_value()
                if prefix_before_right_subtree + current.right.min_prefix_sum <= 0 \
                    <= prefix_before_right_subtree + current.right.max_prefix_sum:
                    prefix_sum += current._get_node_value()
                    current = current.right
                    continue
            if current.left:
                prefix_sum -= current.left.net_inserts
                current = current.left

def test_update_bst():
    update_bst = UpdateBST()
    update_bst.insert(Deletion(6))
    update_bst.insert(Insertion(3, 5))
    update_bst.insert(Insertion(0, 3))
    update_bst.update_added(Insertion(3, 5))
    assert update_bst.find_most_recent_bridge(0) < 0
    assert update_bst.find_most_recent_bridge(2) < 0
    assert 6 < update_bst.find_most_recent_bridge(7) <= 7
    print("test_update_bst() passed")


class PartiallyRetroactivePriorityQueue:
    # assume t and k are unique integers
    def __init__(self):
        self.q_now = []
        self.inserts = InsertionBST()
        self.updates = UpdateBST()
    
    def insert_insertion(self, t, k):
        # assume that every delete-min is already associated with some insert
        entry = Insertion(t, k)
        self.inserts.insert(entry)
        self.updates.insert(entry)

        bridge = self.updates.find_most_recent_bridge(t)
        addition = self.inserts.max_deleted_after(bridge)
        heapq.heappush(self.q_now, addition.k)

        self.inserts.update_added(addition)
        self.updates.update_added(addition)

    def insert_delete_min(self, t):
        # not retroactive; insert deletes before insertions to be safe
        if self.inserts.data:
            print("Warning: insert_delete_min() is not retroactive and could break things now")
        entry = Deletion(t)
        self.updates.insert(entry)

    def insert_insertion_no_qnow(self, t, k):
        # called when there are delete_mins at q_empty times due to insert_insertion assumptions
        entry = Insertion(t, k)
        self.inserts.insert(entry)
        self.updates.insert(entry)

    def remove_delete_min(self, t):
        raise NotImplementedError

    def remove_insertion(self, t, k):
        raise NotImplementedError

    def all(self):
        return self.q_now

def test_priority_queue():
    queue = PartiallyRetroactivePriorityQueue()
    queue.insert_delete_min(8)
    queue.insert_delete_min(3)
    queue.insert_delete_min(7)
    queue.insert_delete_min(11)
    queue.insert_delete_min(10)
    queue.insert_delete_min(12)

    queue.insert_insertion_no_qnow(4, 6)
    queue.insert_insertion_no_qnow(6, 7)
    queue.insert_insertion_no_qnow(5, 2)
    queue.insert_insertion_no_qnow(9, 5)
    queue.insert_insertion_no_qnow(1, 3)
    queue.insert_insertion_no_qnow(2, 1)
    assert len(queue.all()) == 0
    queue.insert_insertion(13, 4)
    
    assert set(queue.all()) == {4}
    queue.insert_insertion(2, 1)
    assert set(queue.all()) == {4, 7}
    print("test_priority_queue() passed")


if __name__ == "__main__":
    test_insertion_bst()
    test_update_bst()
    test_priority_queue()
