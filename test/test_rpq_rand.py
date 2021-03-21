import unittest
import random
import heapq

from rpq import RetroactivePriorityQueue


class RandomRPQTest(unittest.TestCase):
    def setUp(self):
        self.operations = []
        self.rpq = RetroactivePriorityQueue()
        self.verbose = False
        self.test_error = True

    def log(self, s):
        if self.verbose:
            print("OP {}".format(s))

    def dump_state(self):
        if self.verbose:
            print("RPQ STATE:")
            print("    TEST_OP  {}".format(self.operations))
            print("    BRDG     {}".format(list(self.rpq.bridges)))
            print("    SIZE     {}".format(list(self.rpq.size_changes)))
            print("    DEL_INS  {}".format(list(self.rpq.deleted_inserts)))
            print("    INS_IN_Q {}".format(list(self.rpq.inserts_in_q)))

    def verify_q_now(self):
        self.dump_state()
        heap = []
        for t, delta, v in self.operations:
            if delta == 1:
                heapq.heappush(heap, v)
            else:
                heapq.heappop(heap)

        expected_q_now = list(sorted(heap))
        actual_q_now = list(self.rpq)
        self.assertEqual(expected_q_now, actual_q_now)

    def add_insert(self, t, v):
        self.log("add_insert({}, {})".format(t, v))
        if self.t_exists(t):
            if self.test_error:
                self.assertRaises(KeyError, self.rpq.add_insert, t, v)
        else:
            self.operations.insert(self.find_index(t), (t, 1, v))
            self.rpq.add_insert(t, v)

        self.verify_q_now()

    def add_delete_min(self, t):
        self.log("delete_min({})".format(t))
        if self.t_exists(t):
            if self.test_error:
                self.assertRaises(KeyError, self.rpq.add_delete_min, t)
        elif self.is_empty_after(t):
            if self.test_error:
                self.assertRaises(ValueError, self.rpq.add_delete_min, t)
        else:
            self.operations.insert(self.find_index(t), (t, -1, None))
            self.rpq.add_delete_min(t)

        self.verify_q_now()

    def remove(self, t):
        self.log("remove({})".format(t))
        if not self.t_exists(t):
            self.assertRaises(KeyError, self.rpq.remove, t)
        else:
            i = self.find_index(t)
            op = self.operations[i]

            if op[1] > 0 and self.is_empty_after(op[0]):
                if self.test_error:
                    self.assertRaises(ValueError, self.rpq.remove, t)
            else:
                del self.operations[i]
                self.rpq.remove(t)
        self.verify_q_now()

    def t_exists(self, t):
        i = self.find_index(t)
        return i < len(self.operations) and self.operations[i][0] == t

    def find_index(self, t):
        for i, v in enumerate(self.operations):
            if v[0] >= t:
                return i

        return len(self.operations)

    def size_at(self, t):
        return sum(delta for op_t, delta, k in self.operations if op_t <= t)

    def is_empty_after(self, t):
        size = 0
        for op in self.operations:
            if t < op[0] and size == 0:
                return True
            size += op[1]

        return size == 0

    def random_op_sequence(
        self,
        op_cnt,
        max_t = 10 ** 9,
        max_v = 10 ** 9,
        remove_p = 0.4,
        insert_p = 0.7,
        seed = 4
    ):
        rng = random.Random(seed)
        for _ in range(op_cnt):
            remove = rng.random() <= remove_p and len(self.operations) > 0

            if remove:
                op = rng.choice(self.operations)
                self.remove(op[0])
            else:
                t = rng.randrange(max_t)
                if rng.random() <= insert_p:
                    v = rng.randrange(max_v)
                    self.add_insert(t, v)
                else:
                    self.add_delete_min(t)

    def test_no_remove(self):
        self.random_op_sequence(1000, remove_p = -1)

    def test_no_errors(self):
        self.test_error = False
        self.random_op_sequence(1000)

    def test_generic(self):
        self.random_op_sequence(1000)

    def test_many_inserts(self):
        self.random_op_sequence(1000, insert_p = 0.9)

    def test_many_delete_mins(self):
        self.random_op_sequence(1000, insert_p = 0.4)

    def test_key_error(self):
        self.random_op_sequence(1000, max_t = 100)

    def test_repeated_values(self):
        self.random_op_sequence(1000, max_v = 10)
