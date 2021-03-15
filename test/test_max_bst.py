import unittest
from rpq.max_bst import MaxBST

class MaxBSTTest(unittest.TestCase):
    def test(self):
        max_bst = MaxBST()

        max_bst[1] = 5
        self.assertEqual((5, 1), max_bst.agg_after(0))
        self.assertEqual(5, max_bst[1])

        max_bst[2] = 6
        max_bst[-1] = 7

        self.assertEqual((6, 2), max_bst.agg_after(0))
        self.assertEqual((7, -1), max_bst.agg_after(-3))

        max_bst.remove(2)
        self.assertEqual((5, 1), max_bst.agg_after(0))
