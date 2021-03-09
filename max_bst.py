from treap import Treap

class MaxBST(Treap):
    def __init__(self):
        super().__init__(max)

    def __setitem__(self, key, value):
        super().__setitem__(key, (value, key))

    def __getitem__(self, key):
        return super().__getitem__(key)[0]


def test_max_bst():
    max_bst = MaxBST()
    max_bst[1] = 5
    assert max_bst.agg_after(0) == (5, 1)
    assert max_bst[1] == 5
    max_bst[2] = 6
    max_bst[-1] = 7

    assert max_bst.agg_after(0) == (6, 2)
    assert max_bst.agg_after(-3) == (7, -1)
    max_bst.remove(2)
    assert max_bst.agg_after(0) == (5, 1)

    print("test_max_bst() passed")

if __name__ == "__main__":
    test_max_bst()

