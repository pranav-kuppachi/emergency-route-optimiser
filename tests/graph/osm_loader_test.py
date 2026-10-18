
import unittest
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ero.graph.osm_loader import load_road_graph


class TestOSMLoader(unittest.TestCase):

    def test_one_way_road(self):
        osm_data = """\
        <osm>
            <node id="1" lat="11.0000" lon="76.0000"/>
            <node id="2" lat="11.0010" lon="76.0010"/>
            <way id="10">
                <nd ref="1"/>
                <nd ref="2"/>
                <tag k="highway" v="residential"/>
                <tag k="oneway" v="yes"/>
            </way>
        </osm>
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".osm", encoding="utf-8"
        ) as file:
            file.write(osm_data)
            file.flush()

            graph = load_road_graph(file.name)

        self.assertEqual(len(graph.neighbors(1)), 1)
        self.assertEqual(graph.neighbors(1)[0][0], 2)
        self.assertEqual(len(graph.neighbors(2)), 0)

    
    def test_two_way_road(self):
        osm_data = """\
        <osm>
            <node id="1" lat="11.0000" lon="76.0000"/>
            <node id="2" lat="11.0010" lon="76.0010"/>
            <way id="10">
                <nd ref="1"/>
                <nd ref="2"/>
                <tag k="highway" v="residential"/>
            </way>
        </osm>
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".osm", encoding="utf-8"
        ) as file:
            file.write(osm_data)
            file.flush()

            graph = load_road_graph(file.name)

        self.assertEqual(len(graph.neighbors(1)), 1)
        self.assertEqual(len(graph.neighbors(2)), 1)
        self.assertEqual(graph.neighbors(1)[0][0], 2)
        self.assertEqual(graph.neighbors(2)[0][0], 1)


    def test_reverse_one_way_road(self):
        osm_data = """\
        <osm>
            <node id="1" lat="11.0000" lon="76.0000"/>
            <node id="2" lat="11.0010" lon="76.0010"/>
            <way id="10">
                <nd ref="1"/>
                <nd ref="2"/>
                <tag k="highway" v="residential"/>
                <tag k="oneway" v="-1"/>
            </way>
        </osm>
        """

        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".osm", encoding="utf-8"
        ) as file:
            file.write(osm_data)
            file.flush()

            graph = load_road_graph(file.name)

        self.assertEqual(len(graph.neighbors(1)), 0)
        self.assertEqual(len(graph.neighbors(2)), 1)
        self.assertEqual(graph.neighbors(2)[0][0], 1)


if __name__ == "__main__":
    unittest.main()
