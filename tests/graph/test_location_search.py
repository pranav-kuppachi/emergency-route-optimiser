
import unittest

from ero.graph.road_graph import RoadGraph
from ero.graph.location_search import (
    search_locations,
    resolve_to_graph_node,
)


class TestLocationSearch(unittest.TestCase):
    def setUp(self):
        self.index = {
            "places": [
                {
                    "name": "Central Theater",
                    "coordinates": (11.0158, 76.9554),
                    "osm_id": "1",
                    "kind": "place",
                },
                {
                    "name": "RS Puram",
                    "coordinates": (11.0080, 76.9502),
                    "osm_id": "2",
                    "kind": "place",
                },
            ],
            "roads": [
                {
                    "name": "Cross Cut Road",
                    "nodes": [1, 2],
                    "kind": "road",
                }
            ],
        }

        self.graph = RoadGraph()
        self.graph.add_location(
            1, coordinates=(11.0158, 76.9554)
        )
        self.graph.add_location(
            2, coordinates=(11.0080, 76.9502)
        )

    def test_case_insensitive_search(self):
        results = search_locations(self.index, "central theater")
        self.assertEqual(results[0]["name"], "Central Theater")

    def test_partial_search(self):
        results = search_locations(self.index, "RS")
        self.assertTrue(any(r["name"] == "RS Puram" for r in results))

    def test_empty_query_returns_no_results(self):
        self.assertEqual(search_locations(self.index, "  "), [])

    def test_nearest_graph_node(self):
        node, distance = resolve_to_graph_node(
            self.graph, (11.0158, 76.9554)
        )
        self.assertEqual(node, 1)
        self.assertEqual(distance, 0)

    def test_rejects_too_far_location(self):
        with self.assertRaises(ValueError):
            resolve_to_graph_node(
                self.graph, (0.0, 0.0), max_distance=100
            )


if __name__ == "__main__":
    unittest.main()
