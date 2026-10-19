import heapq
import random
import unittest

from ero.queues.radix_heap import RadixHeap


class TestRadixHeap(unittest.TestCase):

    def test_bucket_index(self):
        heap = RadixHeap()
        heap.last = 4
        self.assertEqual(heap._bucket_index(4), 0)
        self.assertEqual(heap._bucket_index(5), 1)
        self.assertEqual(heap._bucket_index(6), 2)
        self.assertEqual(heap._bucket_index(7), 2)

    def test_push_and_expand_buckets(self):
        heap = RadixHeap()
        heap.push(0, "A")
        heap.push(1 << 40, "B")
        self.assertEqual(heap.size, 2)
        self.assertIn((0, "A"), heap.buckets[0])
        self.assertGreater(len(heap.buckets), 40)

    def test_invalid_priorities(self):
        heap = RadixHeap()
        with self.assertRaises(ValueError):
            heap.push(-1, "A")
        with self.assertRaises(TypeError):
            heap.push(2.5, "B")
        heap.last = 4
        with self.assertRaises(ValueError):
            heap.push(3, "C")

    def test_pop_from_empty_heap(self):
        heap = RadixHeap()
        with self.assertRaises(IndexError):
            heap.pop_min()

    def test_pop_in_sorted_order(self):
        heap = RadixHeap()
        for priority in [8, 1, 6, 3, 10]:
            heap.push(priority, str(priority))
        extracted = []
        while not heap.is_empty():
            extracted.append(heap.pop_min()[0])
        self.assertEqual(extracted, [1, 3, 6, 8, 10])
        self.assertEqual(heap.size, 0)

    def test_duplicate_priorities(self):
        heap = RadixHeap()
        heap.push(5, "A")
        heap.push(5, "B")
        results = {heap.pop_min(), heap.pop_min()}
        self.assertEqual(results, {(5, "A"), (5, "B")})
        self.assertTrue(heap.is_empty())

    def test_redistribution(self):
        heap = RadixHeap()
        heap.last = 4
        heap.push(6, "Hospital")
        heap.push(7, "Clinic")
        heap._redistribute(2)
        self.assertEqual(heap.last, 6)
        self.assertIn((6, "Hospital"), heap.buckets[0])
        self.assertIn((7, "Clinic"), heap.buckets[1])
        self.assertEqual(heap.size, 2)

    def test_randomized_operations_against_heapq(self):
        rng = random.Random(42)
        heap = RadixHeap()
        reference = []
        sequence = 0
        for _ in range(500):
            should_push = not reference or rng.random() < 0.65
            if should_push:
                priority = heap.last + rng.randint(0, 100)
                item = f"item-{sequence}"
                heap.push(priority, item)
                heapq.heappush(reference, (priority, sequence, item))
                sequence += 1
            else:
                actual_priority, actual_item = heap.pop_min()
                self.assertEqual(actual_priority, reference[0][0])
                index = next(
                    i for i, entry in enumerate(reference)
                    if entry[2] == actual_item
                )
                self.assertEqual(reference[index][0], actual_priority)
                reference.pop(index)
                heapq.heapify(reference)
            self.assertEqual(heap.size, len(reference))
            self.assertEqual(heap.is_empty(), not reference)
        while reference:
            actual_priority, actual_item = heap.pop_min()
            self.assertEqual(actual_priority, reference[0][0])
            index = next(
                i for i, entry in enumerate(reference)
                if entry[2] == actual_item
            )
            self.assertEqual(reference[index][0], actual_priority)
            reference.pop(index)
            heapq.heapify(reference)
        self.assertTrue(heap.is_empty())
        self.assertEqual(heap.size, 0)


if __name__ == "__main__":
    unittest.main()
