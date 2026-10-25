
"""
Stores the road network as a graph and provides
methods to add locations and roads and retrieve
a location's neighbours.
"""


class RoadGraph:
    def __init__(self):
        self.adjacency_list = {}

        # Additional metadata for location search and map display.
        self.coordinates = {}
        self.location_names = {}
        self.location_tags = {}
        self.road_names = {}

    def add_location(self, location, coordinates=None, name=None, tags=None):
        if location not in self.adjacency_list:
            self.adjacency_list[location] = []

        if coordinates is not None:
            self.coordinates[location] = coordinates

        if name:
            self.location_names[location] = name

        if tags:
            self.location_tags[location] = dict(tags)

    def add_road(
        self, source, destination, distance, bidirectional=True, name=None
    ):
        self.add_location(source)
        self.add_location(destination)

        self.adjacency_list[source].append((destination, distance))

        if name:
            self.road_names[(source, destination)] = name

        if bidirectional:
            self.adjacency_list[destination].append((source, distance))

            if name:
                self.road_names[(destination, source)] = name

    def neighbors(self, location):
        if location not in self.adjacency_list:
            raise KeyError("Location does not exist")
        return self.adjacency_list[location].copy()

    def locations(self):
        return list(self.adjacency_list)

    def __len__(self):
        return len(self.adjacency_list)
