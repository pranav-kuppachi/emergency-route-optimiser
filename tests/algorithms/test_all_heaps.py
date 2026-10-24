#Testing with all the heaps together using a graph that includes
#a route improvement (0 → 1 initially costs 4, but 0 → 2 → 1 costs 3) 
# and an unreachable location, so it tests more than a trivial path.

import unittest

from ero.graph.road_graph import RoadGraph
from ero.algorithms.dijkstra import dijkstra
from ero.queues.binomial_heap import BinomialHeap
from ero.queues.leftist_heap import LeftistHeap
from ero.queues.skew_heap import SkewHeap
from ero.queues.radix_heap import RadixHeap


class TestDijkstraWithAllHeaps(unittest.TestCase):
    def test_all_heaps_return_same_shortest_distances(self):
        graph = RoadGraph()
        graph.add_road(0, 1, 4)
        graph.add_road(0, 2, 1)
        graph.add_road(2, 1, 2)
        graph.add_road(1, 3, 1)
        graph.add_road(2, 3, 5)
        graph.add_road(3, 4, 3)
        graph.add_location(5)
        expected = {0: 0, 1: 3, 2: 1, 3: 4, 4: 7, 5: float("inf"),}
        heaps = [BinomialHeap(), LeftistHeap(), SkewHeap(), RadixHeap(),]
        for heap in heaps:
            with self.subTest(heap=type(heap).__name__):
                result = dijkstra(graph, 0, heap)
                self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
