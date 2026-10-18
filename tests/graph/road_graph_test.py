
import sys
import unittest

sys.path.insert(0, "src")
from ero.graph.road_graph import RoadGraph

class TestRoadGraph(unittest.TestCase):

    def setUp(self):
        self.graph = RoadGraph()

    def test_add_location(self):
        self.graph.add_location(1)

        self.assertEqual(self.graph.locations(), [1])
        self.assertEqual(self.graph.neighbors(1), [])

    def test_add_bidirectional_road(self):
        self.graph.add_road(1, 2, 500)

        self.assertEqual(self.graph.neighbors(1), [(2, 500)])
        self.assertEqual(self.graph.neighbors(2), [(1, 500)])

    def test_add_one_way_road(self):
        self.graph.add_road(1, 2, 500, bidirectional=False)

        self.assertEqual(self.graph.neighbors(1), [(2, 500)])
        self.assertEqual(self.graph.neighbors(2), [])

    def test_locations_and_length(self):
        self.graph.add_location(1)
        self.graph.add_location(2)
        self.graph.add_location(3)

        self.assertEqual(self.graph.locations(), [1, 2, 3])
        self.assertEqual(len(self.graph), 3)


if __name__ == "__main__":
    unittest.main()
