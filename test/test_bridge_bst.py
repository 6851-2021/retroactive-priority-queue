import unittest
from rpq.bridge_bst import BridgeBST

class BridgeBSTTest(unittest.TestCase):
    def test(self):
        bst = BridgeBST()
        bst[6] = -1
        bst[3] = 0
        bst[0] = 1
        self.assertEqual(0, bst.bridge_before(5))
        self.assertEqual(6, bst.bridge_after(5))

        self.assertEqual(7, bst.bridge_before(7))
        self.assertEqual(7, bst.bridge_after(7))

        self.assertEqual(6, bst.bridge_before(6))
        self.assertEqual(6, bst.bridge_after(6))

        self.assertEqual(-20, bst.bridge_before(-20))
        self.assertEqual(-20, bst.bridge_after(-20))
