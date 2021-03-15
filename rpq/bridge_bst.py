from .treap import Treap

class BridgeBSTAggregator:
    def __init__(self, key, value):
        self.sum = value
        self.min_key = key

        self.min_prefix_sum = value
        self.min_prefix_first_key = key
        self.min_prefix_last_key = key

    def __add__(self, other):
        res = BridgeBSTAggregator(None, 0)
        res.sum = self.sum + other.sum
        res.min_key = min(self.min_key, other.min_key)

        other_min_prefix_sum = self.sum + other.min_prefix_sum
        res.min_prefix_sum = min(self.min_prefix_sum, other_min_prefix_sum)

        if self.min_prefix_sum <= res.min_prefix_sum:
            res.min_prefix_first_key = self.min_prefix_first_key
        else:
            res.min_prefix_first_key = other.min_prefix_first_key

        if other_min_prefix_sum <= res.min_prefix_sum:
            res.min_prefix_last_key = other.min_prefix_last_key
        else:
            res.min_prefix_last_key = self.min_prefix_last_key

        return res

class BridgeBST(Treap):
    def __init__(self):
        super().__init__(lambda x, y: x + y)

    def bridge_before(self, key):
        res = self.agg_before(key, include_eq=True)

        if res is None:
            return key
        elif res.min_prefix_sum > 0:
            return min(res.min_key, key)
        elif res.sum == 0:
            return max(res.min_prefix_last_key, key)
        else:
            return res.min_prefix_last_key

    def bridge_after(self, key):
        after_res = self.agg_after(key, include_eq=True)
        if after_res is None:
            return key

        before_sum = self.agg().sum - after_res.sum
        if before_sum == 0:
            return key

        prefix_sum = before_sum + after_res.min_prefix_sum
        assert prefix_sum == 0
        return after_res.min_prefix_first_key

    def __getitem__(self, key):
        return super().__getitem__(key).sum

    def __setitem__(self, key, value):
        super().__setitem__(key, BridgeBSTAggregator(key, value))

    def __iter__(self):
        for k, v in super().__iter__():
            yield k, v.sum