
import heapq
import unittest

from ero.algorithms.dijkstra import dijkstra
from ero.graph.road_graph import RoadGraph


class TestHeap:
    """
    A small adapter around Python's built-in heapq.

    We use this only to test Dijkstra before connecting
    our four custom heap implementations.
    """

    def __init__(self):
        self.items = []

    def push(self, priority, item):
        heapq.heappush(self.items, (priority, item))

    def pop_min(self):
        return heapq.heappop(self.items)

    def is_empty(self):
        return len(self.items) == 0


class TestDijkstra(unittest.TestCase):

    def test_shortest_distances(self):
        # Create a small road network.
        graph = RoadGraph()
        graph.add_road("A", "B", 4)
        graph.add_road("A", "C", 10)
        graph.add_road("B", "C", 3)
        graph.add_road("B", "D", 8)
        graph.add_road("C", "D", 2)

        # Calculate shortest distances starting from A.
        distances = dijkstra(graph, "A", TestHeap())

        # The shortest routes should be:
        # A -> A = 0
        # A -> B = 4
        # A -> B -> C = 7
        # A -> B -> C -> D = 9
        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 4)
        self.assertEqual(distances["C"], 7)
        self.assertEqual(distances["D"], 9)

    def test_unreachable_location(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 5)
        graph.add_location("C")

        distances = dijkstra(graph, "A", TestHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 5)
        self.assertEqual(distances["C"], float("inf"))

    def test_improved_route(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 10)
        graph.add_road("A", "C", 2)
        graph.add_road("C", "B", 3)

        distances = dijkstra(graph, "A", TestHeap())

        # B is first discovered at 10, then improved to 5.
        self.assertEqual(distances["B"], 5)
        self.assertEqual(distances["C"], 2)

    def test_invalid_start(self):
        graph = RoadGraph()
        graph.add_location("A")

        with self.assertRaises(KeyError):
            dijkstra(graph, "Z", TestHeap())


if __name__ == "__main__":
    unittest.main()
