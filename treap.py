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

        return root, s_left
    else:
        s_left, s_right = split(root.left, key, eq_left)
        root.left = s_right
        root.update_aggregate()

        return s_left, root

def merge(left, right):
    if left is None or right is None:
        return left if right is None else right
    elif left.p < right.p:
        left.right = merge(left.right, right)
        left.update_aggregate()
        return left
    else:
        right.left = merge(left, right.left)
        right.update_aggregate()
        return right

def insert(root, node):
    left, node_and_right = split(root, node.key)
    old_node, right = split(node_and_right, node.key, eq_left=True)
    return merge(left, merge(node, right))

def remove(root, key):
    if root is None:
        return None
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
        self.agg_f = agg_f
        self.root = None

    def remove(self, key):
        self.root = remove(self.root, key)

    def agg_before(self, key, include_eq = False):
        before, after = split(self.root, key, eq_left = include_eq)
        result = before.agg if before is not None else None
        self.root = merge(before, after)
        return result

    def agg_after(self, key, include_eq = False):
        before, after = split(self.root, key, eq_left = not include_eq)
        result = after.agg if after is not None else None
        self.root = merge(before, after)
        return result

    def agg(self):
        return self.root.agg if self.root else None

    def __getitem__(self, key):
        return find(self.root, key)

    def __setitem__(self, key, value):
        node = Node(key, value, self.agg_f)
        self.root = insert(self.root, node)

    def __iter__(self):
        if self.root is not None:
            yield from self.root

