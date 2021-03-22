import random
random.seed(3)

class Node:
    def __init__(self, key, value, agg_f):
        self.key = key
        self.value = value
        self.p = random.random()
        self.agg_f = agg_f
        self.agg = value

        self.left = None
        self.right = None

    def update_aggregate(self):
        self.agg = self.value
        res = None
        for v in [self.left, self, self.right]:
            if v is None:
                continue
            elif res is None:
                res = v.agg
            else:
                res = self.agg_f(res, v.agg)

        self.agg = res

    def __iter__(self):
        if self.left is not None:
            yield from self.left

        yield self.key, self.value

        if self.right is not None:
            yield from self.right

    def __str__(self):
        return (
            "Node(k:{0.key} v:{0.value} agg:{0.agg} "
            + "left:{0.left} right:{0.right})"
        ).format(self)

def split(root, key, eq_left=False):
    if root is None:
        return None, None

    root_in_left = (
        root.key < key
        or root.key == key and eq_left
    )
    if root_in_left:
        s_left, s_right = split(root.right, key, eq_left)
        root.right = s_left
        root.update_aggregate()
        assert root.right is not root

        return root, s_right
    else:
        s_left, s_right = split(root.left, key, eq_left)
        root.left = s_right
        root.update_aggregate()

        assert root.left is not root
        return s_left, root

def merge(left, right):
    if left is None:
        return right
    elif right is None:
        return left
    elif left.p < right.p:
        left.right = merge(left.right, right)
        left.update_aggregate()
        return left
    else:
        right.left = merge(left, right.left)
        right.update_aggregate()
        return right

def remove(root, key):
    if root is None:
        raise KeyError
    elif root.key == key:
        return merge(root.left, root.right)
    else:
        if key < root.key:
            root.left = remove(root.left, key)
        else:
            root.right = remove(root.right, key)
        root.update_aggregate()
        return root

def find(root, key):
    if root is None:
        raise KeyError
    elif key == root.key:
        return root.value
    elif key < root.key:
        return find(root.left, key)
    else:
        return find(root.right, key)

class Treap:
    def __init__(self, agg_f):
        self._agg_f = agg_f
        self._root = None
        self._len = 0

    def remove(self, key):
        self._root = remove(self._root, key)
        self._len -= 1

    def agg_before(self, key, include_eq = False):
        before, after = split(self._root, key, eq_left = include_eq)
        result = before.agg if before is not None else None
        self._root = merge(before, after)
        return result

    def agg_after(self, key, include_eq = False):
        before, after = split(self._root, key, eq_left = not include_eq)
        result = after.agg if after is not None else None
        self._root = merge(before, after)
        return result

    def agg(self):
        return self._root.agg if self._root else None

    def __getitem__(self, key):
        return find(self._root, key)

    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        left, node_and_right = split(self._root, key)
        old_node, right = split(node_and_right, key, eq_left=True)

        if old_node is None:
            self._len += 1

        node = Node(key, value, self._agg_f)
        self._root = merge(left, merge(node, right))

    def __len__():
        return self._len

    def __iter__(self):
        if self._root is not None:
            yield from self._root

