
import heapq
import unittest

from ero.algorithms.dijkstra import dijkstra
from ero.graph.road_graph import RoadGraph
from ero.queues.radix_heap import RadixHeap


class TestHeap:
    """Simple heapq adapter for testing Dijkstra independently."""

    def __init__(self):
        self.items = []

    def push(self, priority, item):
        heapq.heappush(self.items, (priority, item))

    def pop_min(self):
        return heapq.heappop(self.items)

    def is_empty(self):
        return len(self.items) == 0


class TestDijkstra(unittest.TestCase):

    def setUp(self):
        self.graph = RoadGraph()
        self.graph.add_road("A", "B", 4)
        self.graph.add_road("A", "C", 10)
        self.graph.add_road("B", "C", 3)
        self.graph.add_road("B", "D", 8)
        self.graph.add_road("C", "D", 2)

    def test_shortest_distances(self):
        distances = dijkstra(self.graph, "A", TestHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 4)
        self.assertEqual(distances["C"], 7)
        self.assertEqual(distances["D"], 9)

    def test_unreachable_location(self):
        self.graph.add_location("E")

        distances = dijkstra(self.graph, "A", TestHeap())

        self.assertEqual(distances["E"], float("inf"))

    def test_improved_route(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 10)
        graph.add_road("A", "C", 2)
        graph.add_road("C", "B", 3)

        distances = dijkstra(graph, "A", TestHeap())

        self.assertEqual(distances["B"], 5)
        self.assertEqual(distances["C"], 2)

    def test_invalid_start(self):
        with self.assertRaises(KeyError):
            dijkstra(self.graph, "Z", TestHeap())

    def test_radix_heap_integration(self):
        self.graph.add_location("E")

        distances = dijkstra(self.graph, "A", RadixHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 4)
        self.assertEqual(distances["C"], 7)
        self.assertEqual(distances["D"], 9)
        self.assertEqual(distances["E"], float("inf"))

    def test_directed_roads(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 5, bidirectional=False)
        graph.add_road("B", "C", 3, bidirectional=False)

        forward = dijkstra(graph, "A", RadixHeap())
        backward = dijkstra(graph, "C", RadixHeap())

        self.assertEqual(forward["C"], 8)
        self.assertEqual(backward["A"], float("inf"))


if __name__ == "__main__":
    unittest.main()
