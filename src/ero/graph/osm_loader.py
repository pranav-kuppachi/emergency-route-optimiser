"""
Takes real OSM data and converts its locations
and roads into our RoadGraph structure and returns
the resulting graph.
"""
import xml.etree.ElementTree as ET #Python's inbuilt XML parser to read .osm file 
from pathlib import Path #helps us work with filepaths easily
import math #Python's math library for Haversine formula, which calculates the approximate distance between two geographic coordinates while accounting for Earth's curvature.
from ero.graph.road_graph import RoadGraph #to fill the graph structure that is alr implemented.

def read_osm_file(file_path): #Read .osm file and return it's root element
    tree = ET.parse(file_path)
    root = tree.getroot() #Gets outermost osm element
    return root

def extract_nodes(root): #Extracts node id's and their coordinates from OSM data.
    nodes = {}
    for element in root.findall("node"):
        node_id = element.get("id")
        latitude = float(element.get("lat"))
        longitude = float(element.get("lon"))
        nodes[node_id] = (latitude, longitude)
    return nodes

def extract_road_ways(root): #Extracts road ways and it's data from OSM
    road_ways = []
    #Using this cuz OSM also contains footpaths, cycleways, steps and other features.
    allowed_roads = {
        "motorway", "trunk", "primary", "secondary", "tertiary",
        "unclassified", "residential", "service", "living_street",
        "motorway_link", "trunk_link", "primary_link",
        "secondary_link", "tertiary_link"
    }

    for way in root.findall("way"):
        road_type = None
        node_ids = [] #stores the node IDs in road order.
        tags = {} #stores the way's descriptive tags as key-value pairs.

        for tag in way.findall("tag"): #tag is the xml element itself
            tags[tag.get("k")] = tag.get("v") #k and v are key n value

        road_type = tags.get("highway")
        if road_type not in allowed_roads:
            continue

        for node in way.findall("nd"): #nd means node that comes along the way
            node_ids.append(node.get("ref")) #id of referenced node

        if len(node_ids) >= 2: #Check that the way has enough nodes cuz oad segment needs at least two nodes to connect locations.
            road_ways.append({"node_ids": node_ids, "tags": tags})

    return road_ways

def calculate_distance(point1, point2):
    latitude1, longitude1 = point1
    latitude2, longitude2 = point2
    #math.radians() converts degrees into radians because Python's trigonometric functions use radians.
    latitude1 = math.radians(latitude1) 
    longitude1 = math.radians(longitude1)
    latitude2 = math.radians(latitude2)
    longitude2 = math.radians(longitude2)

    latitude_difference = latitude2 - latitude1
    longitude_difference = longitude2 - longitude1

    a = (math.sin(latitude_difference / 2) ** 2 + math.cos(latitude1)* math.cos(latitude2) * math.sin(longitude_difference / 2) ** 2)
    #6371000 is Earth's approximate radius in metres. 
    # The formula returns the straight-line distance between two points,
    # not the distance a vehicle travels along a curved road.  
    distance = 6371000 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return max(1, round(distance))

def load_road_graph(file_path): #Load OSM file and return RoadGraph
    root = read_osm_file(file_path)
    nodes = extract_nodes(root)
    road_ways = extract_road_ways(root)

    graph = RoadGraph()

    for way in road_ways:
        for node_id in way["node_ids"]:
            graph.add_location(int(node_id))

    for way in road_ways:
        node_ids = way["node_ids"]
        tags = way["tags"]
        one_way = tags.get("oneway") == "yes"
        reverse_one_way = tags.get("oneway") == "-1"

        for i in range(len(node_ids) - 1):
            source = node_ids[i]
            destination = node_ids[i + 1]

            if source not in nodes or destination not in nodes:
                continue

            distance = calculate_distance(nodes[source], nodes[destination])

            if reverse_one_way:
                graph.add_road(int(destination),int(source),distance,bidirectional=False)
            else:
                graph.add_road(int(source), int(destination), distance, bidirectional=not one_way)
    return graph
            
