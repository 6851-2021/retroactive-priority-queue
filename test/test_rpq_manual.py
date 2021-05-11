import unittest
from rpq.rpq import RetroactivePriorityQueue

class PriorityQueueManualTest(unittest.TestCase):
    def test_simple(self):
        queue = RetroactivePriorityQueue()
        self.assertEqual([], list(queue))

        queue.add_insert(0, 5)
        self.assertEqual([5], list(queue))

        queue.add_insert(10, 3)
        self.assertEqual([3, 5], list(queue))

        queue.add_delete_min(5)
        self.assertEqual([3], list(queue))

        queue.add_insert(2, 7)
        self.assertEqual([3, 7], list(queue))

        queue.add_insert(3, 4)
        self.assertEqual([3, 5, 7], list(queue))

        queue.add_delete_min(7)
        self.assertEqual([3, 7], list(queue))

        # delete insert
        queue.remove(2)
        self.assertEqual([3], list(queue))

        # delete delete
        queue.remove(5)
        self.assertEqual([3, 5], list(queue))

    def test_get_min(self):
        queue = RetroactivePriorityQueue()
        self.assertEqual(None, queue.get_min())

        queue.add_insert(2, 3)
        queue.add_insert(5, 8)
        self.assertEqual(3, queue.get_min())

        queue.remove(2)
        self.assertEqual(8, queue.get_min())
