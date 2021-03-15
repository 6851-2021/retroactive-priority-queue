from .treap import Treap

class MaxBST(Treap):
    def __init__(self):
        super().__init__(max)

    def __setitem__(self, key, value):
        super().__setitem__(key, (value, key))

    def __getitem__(self, key):
        return super().__getitem__(key)[0]
