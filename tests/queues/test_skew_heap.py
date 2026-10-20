import unittest
from ero.queues.skew_heap import SkewHeap
from ero.algorithms.dijkstra import dijkstra
from ero.graph.road_graph import RoadGraph


class TestSkewHeap(unittest.TestCase):

    def test_empty_heap(self):
        heap = SkewHeap()
        self.assertTrue(heap.is_empty())

        with self.assertRaises(IndexError):
            heap.pop_min()

    def test_single_element(self):
        heap = SkewHeap()
        heap.push(5, "hospital")
        self.assertEqual(heap.pop_min(), (5, "hospital"))
        self.assertTrue(heap.is_empty())

    def test_priority_order(self):
        heap = SkewHeap()

        for priority in [8, 3, 10, 1, 6, 2]:
            heap.push(priority, priority)

        result = []
        while not heap.is_empty():
            result.append(heap.pop_min()[0])

        self.assertEqual(result, [1, 2, 3, 6, 8, 10])

    def test_duplicate_priorities(self):
        heap = SkewHeap()
        heap.push(2, "A")
        heap.push(2, "B")
        heap.push(1, "C")

        result = [heap.pop_min(), heap.pop_min(), heap.pop_min()]

        self.assertEqual([x[0] for x in result], [1, 2, 2])
        self.assertEqual(
            sorted(x[1] for x in result),
            ["A", "B", "C"]
        )

    def test_increasing_priorities(self):
        heap = SkewHeap()

        for i in range(20):
            heap.push(i, i)

        result = [heap.pop_min()[0] for _ in range(20)]
        self.assertEqual(result, list(range(20)))

    def test_decreasing_priorities(self):
        heap = SkewHeap()

        for i in range(20, 0, -1):
            heap.push(i, i)

        result = [heap.pop_min()[0] for _ in range(20)]
        self.assertEqual(result, list(range(1, 21)))

    def test_insert_after_emptying(self):
        heap = SkewHeap()
        heap.push(3, "A")
        self.assertEqual(heap.pop_min(), (3, "A"))

        heap.push(1, "B")
        self.assertEqual(heap.pop_min(), (1, "B"))
        self.assertTrue(heap.is_empty())
    def test_dijkstra_integration(self):
        graph = RoadGraph()

        graph.add_road("A", "B", 4)
        graph.add_road("A", "C", 10)
        graph.add_road("B", "C", 3)
        graph.add_road("B", "D", 8)
        graph.add_road("C", "D", 2)

        distances = dijkstra(graph, "A", SkewHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 4)
        self.assertEqual(distances["C"], 7)
        self.assertEqual(distances["D"], 9)


if __name__ == "__main__":
    unittest.main()
