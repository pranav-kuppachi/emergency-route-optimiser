
import unittest

from ero.algorithms.dijkstra import dijkstra
from ero.graph.road_graph import RoadGraph
from ero.queues.binomial_heap import BinomialHeap


class TestBinomialHeapDijkstra(unittest.TestCase):

    def test_shortest_distances(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 4)
        graph.add_road("A", "C", 10)
        graph.add_road("B", "C", 3)
        graph.add_road("B", "D", 8)
        graph.add_road("C", "D", 2)

        distances = dijkstra(graph, "A", BinomialHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 4)
        self.assertEqual(distances["C"], 7)
        self.assertEqual(distances["D"], 9)

    def test_improved_route(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 10)
        graph.add_road("A", "C", 2)
        graph.add_road("C", "B", 3)

        distances = dijkstra(graph, "A", BinomialHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 5)
        self.assertEqual(distances["C"], 2)

    def test_unreachable_location(self):
        graph = RoadGraph()
        graph.add_road("A", "B", 5)
        graph.add_location("C")

        distances = dijkstra(graph, "A", BinomialHeap())

        self.assertEqual(distances["A"], 0)
        self.assertEqual(distances["B"], 5)
        self.assertEqual(distances["C"], float("inf"))


if __name__ == "__main__":
    unittest.main()
