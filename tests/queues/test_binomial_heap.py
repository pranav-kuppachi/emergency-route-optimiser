
import unittest

from ero.queues.binomial_heap import BinomialHeap


class TestBinomialHeap(unittest.TestCase):

    def test_empty_heap(self):
        heap = BinomialHeap()

        self.assertTrue(heap.is_empty())

        with self.assertRaises(IndexError):
            heap.pop_min()

    def test_push_and_pop_single_item(self):
        heap = BinomialHeap()

        heap.push(10, "A")

        self.assertFalse(heap.is_empty())
        self.assertEqual(heap.pop_min(), (10, "A"))
        self.assertTrue(heap.is_empty())

    def test_pop_in_priority_order(self):
        heap = BinomialHeap()

        heap.push(12, "A")
        heap.push(3, "B")
        heap.push(8, "C")
        heap.push(1, "D")
        heap.push(5, "E")

        result = [heap.pop_min() for _ in range(5)]

        self.assertEqual(
            result,
            [(1, "D"), (3, "B"), (5, "E"), (8, "C"), (12, "A")]
        )
        self.assertTrue(heap.is_empty())

    def test_duplicate_priorities(self):
        heap = BinomialHeap()

        heap.push(4, "A")
        heap.push(4, "B")
        heap.push(2, "C")

        result = [heap.pop_min() for _ in range(3)]

        self.assertEqual(result[0], (2, "C"))
        self.assertEqual(sorted(p for p, _ in result), [2, 4, 4])
        self.assertEqual({item for _, item in result}, {"A", "B", "C"})

    def test_insert_after_removing_all_items(self):
        heap = BinomialHeap()

        heap.push(7, "A")
        self.assertEqual(heap.pop_min(), (7, "A"))
        self.assertTrue(heap.is_empty())

        heap.push(2, "B")
        self.assertEqual(heap.pop_min(), (2, "B"))
        self.assertTrue(heap.is_empty())

    def test_decreasing_priorities(self):
        heap = BinomialHeap()

        for priority in range(20, 0, -1):
            heap.push(priority, priority)

        result = [heap.pop_min()[0] for _ in range(20)]

        self.assertEqual(result, list(range(1, 21)))

    def test_increasing_priorities(self):
        heap = BinomialHeap()

        for priority in range(1, 21):
            heap.push(priority, priority)

        result = [heap.pop_min()[0] for _ in range(20)]

        self.assertEqual(result, list(range(1, 21)))


if __name__ == "__main__":
    unittest.main()
