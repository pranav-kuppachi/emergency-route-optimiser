
import unittest

from ero.algorithms.shortest_path import (
    dijkstra_with_predecessors,
    reconstruct_path,
)
from ero.graph.road_graph import RoadGraph
from ero.queues.radix_heap import RadixHeap


class TestShortestPath(unittest.TestCase):

    def setUp(self):
        self.graph = RoadGraph()
        self.graph.add_road("A", "B", 4)
        self.graph.add_road("A", "C", 10)
        self.graph.add_road("B", "C", 3)
        self.graph.add_road("C", "D", 2)
        self.graph.add_location("E")

    def test_reconstructs_shortest_path(self):
        distances, predecessors = dijkstra_with_predecessors(
            self.graph, "A", RadixHeap()
        )

        path = reconstruct_path(predecessors, "A", "D")

        self.assertEqual(path, ["A", "B", "C", "D"])
        self.assertEqual(distances["D"], 9)

    def test_unreachable_destination(self):
        distances, predecessors = dijkstra_with_predecessors(
            self.graph, "A", RadixHeap()
        )

        path = reconstruct_path(predecessors, "A", "E")

        self.assertEqual(distances["E"], float("inf"))
        self.assertEqual(path, [])

    def test_source_equals_destination(self):
        distances, predecessors = dijkstra_with_predecessors(
            self.graph, "A", RadixHeap()
        )

        path = reconstruct_path(predecessors, "A", "A")

        self.assertEqual(path, ["A"])


if __name__ == "__main__":
    unittest.main()
