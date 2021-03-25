from .treap import Treap

class MinPrefixSumAggregator:
    def __init__(self, key, value):
        self.sum = value
        self.min_key = key
        self.max_key = key

        self.min_prefix_sum = value
        self.min_prefix_first_key = key
        self.min_prefix_last_key = key

    def __add__(self, other):
        res = MinPrefixSumAggregator(None, 0)
        res.sum = self.sum + other.sum
        res.min_key = self.min_key
        res.max_key = other.max_key

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

class ZeroPrefixBST(Treap):
    def __init__(self):
        super().__init__(lambda x, y: x + y)

    def zero_prefix_before(self, key):
        # Returns the maximum k <= key such that the values of all operations
        # with keys <k sum up to 0
        res = self.agg_before(key, include_eq=False)

        if res is None:
            return key
        elif res.min_prefix_sum > 0:
            return min(res.min_key, key)
        elif res.sum == 0:
            return max(res.min_prefix_last_key, key)
        else:
            return res.min_prefix_last_key

    def zero_prefix_after(self, key):
        # Returns the minimum k >= key such that the values of all operations
        # with keys <= k sum to 0 (and None if no such k exists)

        after_res = self.agg_after(key, include_eq=False)
        if after_res is None:
            return key

        before_sum = self.agg().sum - after_res.sum
        min_prefix_in_res = before_sum + after_res.min_prefix_sum

        if before_sum == 0:
            return key
        elif min_prefix_in_res == 0:
            return after_res.min_prefix_first_key
        else:
            return None

    def __getitem__(self, key):
        return super().__getitem__(key).sum

    def __setitem__(self, key, value):
        super().__setitem__(key, MinPrefixSumAggregator(key, value))

    def __iter__(self):
        for k, v in super().__iter__():
            yield k, v.sum
