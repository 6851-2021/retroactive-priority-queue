import treap

class PrefixSumAggregator:
    def __init__(self, key, value):
        self.sum = value
        self.min_prefix_sum = value
        self.min_prefix_key = key

        self.min_suffix_sum = value
        self.min_suffix_key = key

    def __add__(self, other):
        res = PrefixSumAggregator(None, 0)
        res.sum = self.sum + other.sum

        # In case of ties, take the longer prefix / suffix

        other_prefix_sum = other.min_prefix_sum + self.sum
        if self.min_prefix_sum < other_prefix_sum:
            res.min_prefix_sum = self.min_prefix_sum
            res.min_prefix_key = self.min_prefix_key
        else:
            res.min_prefix_sum = other_prefix_sum
            res.min_prefix_key = other.min_prefix_key

        self_suffix_sum = self.min_suffix_sum + other.sum
        if other.min_prefix_sum < self_suffix_sum:
            res.min_suffix_sum = other.min_prefix_sum
            res.min_suffix_key = other.min_prefix_key
        else:
            res.min_prefix_sum = self_suffix_sum
            res.min_prefix_key = self.min_prefix_key

        return res

class UpdateBST:
    def __init__(self):
        super().__init__(sum)

    def bridge_before(self, key):
        res = self.agg_before(key)
        return res.min_prefix_key if res is None else None

    def bridge_after(self, key):
        res = self.agg_after(key)
        return res.min_suffx_key if res is None else None

    def __getitem__(self, key):
        return find(self.root, key).sum

    def __setitem__(self, key, value):
        super().__setitem__(key, PrefixSumAggregator(key, value))

    def __iter__(self):
        if self.root is not None:
            for v in self.root:
                yield v.sum
