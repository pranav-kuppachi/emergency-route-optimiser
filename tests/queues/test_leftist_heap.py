import unittest

from ero.queues.leftist_heap import LeftistHeap
from ero.algorithms.dijkstra import dijkstra
from ero.graph.road_graph import RoadGraph

class TestLeftistHeap(unittest.TestCase):
    def check_invariants(self, heap, node):
        if node is None:
            return

        left_npl = heap._get_npl(node.left)
        right_npl = heap._get_npl(node.right)

        self.assertGreaterEqual(left_npl, right_npl)

        expected_npl = 1 + min(left_npl, right_npl)
        self.assertEqual(node.npl, expected_npl)

        if node.left is not None:
            self.assertLessEqual(node.priority, node.left.priority)

        if node.right is not None:
            self.assertLessEqual(node.priority, node.right.priority)

        self.check_invariants(heap, node.left)
        self.check_invariants(heap, node.right)
    def test_invariants_after_many_insertions(self):
        heap = LeftistHeap()

        for priority in [8, 3, 5, 1, 7, 2, 9, 4, 6]:
            heap.push(priority, priority * 10)
            self.check_invariants(heap, heap.root)

        while not heap.is_empty():
            heap.pop_min()
            self.check_invariants(heap, heap.root)

    def test_empty_heap(self):
        heap = LeftistHeap()

        self.assertTrue(heap.is_empty())

        with self.assertRaises(IndexError):
            heap.pop_min()

    def test_single_element(self):
        heap = LeftistHeap()
        heap.push(5, 100)

        self.assertFalse(heap.is_empty())
        self.assertEqual(heap.pop_min(), (5, 100))
        self.assertTrue(heap.is_empty())

    def test_minimum_extraction(self):
        heap = LeftistHeap()

        heap.push(8, 80)
        heap.push(3, 30)
        heap.push(5, 50)

        self.assertEqual(heap.pop_min(), (3, 30))
        self.assertEqual(heap.pop_min(), (5, 50))
        self.assertEqual(heap.pop_min(), (8, 80))

        self.assertTrue(heap.is_empty())
    def test_increasing_priorities(self):
        heap = LeftistHeap()

        for priority in [1, 2, 3, 4, 5]:
            heap.push(priority, priority * 10)

        result = [heap.pop_min() for _ in range(5)]

        self.assertEqual(
            result,
            [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]
        )

    def test_decreasing_priorities(self):
        heap = LeftistHeap()

        for priority in [5, 4, 3, 2, 1]:
            heap.push(priority, priority * 10)

        result = [heap.pop_min() for _ in range(5)]

        self.assertEqual(
            result,
            [(1, 10), (2, 20), (3, 30), (4, 40), (5, 50)]
        )

    def test_duplicate_priorities_and_items(self):
        heap = LeftistHeap()

        heap.push(4, 100)
        heap.push(4, 100)
        heap.push(2, 100)
        heap.push(4, 200)

        result = [heap.pop_min() for _ in range(4)]

        self.assertEqual(
            result,
            [(2, 100), (4, 100), (4, 100), (4, 200)]
        )

    def test_repeated_insertion_and_extraction(self):
        heap = LeftistHeap()

        for _ in range(3):
            for priority in [7, 2, 9, 1, 5]:
                heap.push(priority, priority)

            result = [heap.pop_min() for _ in range(5)]

            self.assertEqual(result,
            [(1, 1), (2, 2), (5, 5), (7, 7), (9, 9)])
            self.assertTrue(heap.is_empty())
    def test_merge_swaps_children(self):
        heap = LeftistHeap()

        heap.push(4, 40)
        heap.push(2, 20)

        self.assertEqual(heap.root.priority, 2)
        self.assertIsNotNone(heap.root.left)
        self.assertIsNone(heap.root.right)

        self.assertEqual(heap.root.left.priority, 4)
        self.assertEqual(heap.root.npl, 0)

        self.check_invariants(heap, heap.root)
    def test_negative_priority_rejected(self):
        heap = LeftistHeap()

        with self.assertRaises(ValueError):
            heap.push(-1, 100)

        self.assertTrue(heap.is_empty())

    def test_non_integer_priority_rejected(self):
        heap = LeftistHeap()

        with self.assertRaises(TypeError):
            heap.push(2.5, 100)

        self.assertTrue(heap.is_empty())
    def test_larger_sequence_of_operations(self):
        heap = LeftistHeap()

        priorities = [
            42, 17, 8, 99, 23, 1, 64, 12, 37, 5,
            81, 3, 56, 19, 7, 30, 2, 90, 14, 11
        ]

        for priority in priorities:
            heap.push(priority, priority * 10)
            self.check_invariants(heap, heap.root)

        expected = sorted(priorities)

        for priority in expected:
            self.assertEqual(heap.pop_min(), (priority, priority * 10))
            self.check_invariants(heap, heap.root)

        self.assertTrue(heap.is_empty())
    def test_dijkstra_integration(self):
        graph = RoadGraph()

        graph.add_road("A", "B", 4)
        graph.add_road("A", "C", 10)
        graph.add_road("B", "C", 3)
        graph.add_road("B", "D", 8)
        graph.add_road("C", "D", 2)

        distances = dijkstra(graph, "A", LeftistHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 4)
        self.assertEqual(distances["C"], 7)
        self.assertEqual(distances["D"], 9)


if __name__ == "__main__":
    unittest.main()