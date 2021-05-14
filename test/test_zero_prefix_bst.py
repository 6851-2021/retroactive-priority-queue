import unittest
from retropq.zero_prefix_bst import ZeroPrefixBST

class ZeroPrefixBSTTest(unittest.TestCase):
    def test(self):
        bst = ZeroPrefixBST()
        bst[6] = -1
        bst[3] = 0
        bst[0] = 1
        self.assertEqual(0, bst.zero_prefix_before(5))
        self.assertEqual(6, bst.zero_prefix_after(5))

        self.assertEqual(7, bst.zero_prefix_before(7))
        self.assertEqual(7, bst.zero_prefix_after(7))

        self.assertEqual(0, bst.zero_prefix_before(6))
        self.assertEqual(6, bst.zero_prefix_after(6))

        self.assertEqual(-20, bst.zero_prefix_before(-20))
        self.assertEqual(-20, bst.zero_prefix_after(-20))
