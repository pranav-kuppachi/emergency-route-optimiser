
"""Search named OSM places and roads and resolve them to graph nodes."""

from ero.graph.osm_loader import (
    read_osm_file,
    extract_nodes,
    extract_road_ways,
    calculate_distance,
)


def build_location_index(file_path, graph):
    """Build searchable places and roads from OSM data."""
    root = read_osm_file(file_path)
    nodes = extract_nodes(root)
    road_ways = extract_road_ways(root)

    places = []
    roads = []

    # Include named OSM nodes, even if they aren't road intersections.
    for node_id, node in nodes.items():
        tags = node["tags"]
        name = tags.get("name")

        if name:
            places.append({
                "name": name,
                "coordinates": node["coordinates"],
                "osm_id": node_id,
                "kind": "place",
            })

    # Include named roads and their road-network nodes.
    for way in road_ways:
        name = way["tags"].get("name")
        if not name:
            continue

        way_nodes = [
            int(node_id)
            for node_id in way["node_ids"]
            if node_id in nodes and int(node_id) in graph.adjacency_list
        ]

        if way_nodes:
            roads.append({
                "name": name,
                "nodes": way_nodes,
                "kind": "road",
            })

    return {"places": places, "roads": roads}


def search_locations(index, query, limit=10):
    """Return case-insensitive partial matches for a place or road."""
    query = query.strip().casefold()

    if not query:
        return []

    results = []

    for place in index["places"]:
        if query in place["name"].casefold():
            results.append(place)

    for road in index["roads"]:
        if query in road["name"].casefold():
            results.append(road)

    # Prefer exact name matches, then alphabetical order.
    results.sort(
        key=lambda item: (
            item["name"].casefold() != query,
            item["name"].casefold(),
            item["kind"],
        )
    )

    return results[:limit]



def resolve_to_graph_node(graph, coordinates, max_distance=1000):
    """Find the nearest routable node within max_distance metres."""
    nearest_node = None
    nearest_distance = float("inf")

    for node_id, node_coordinates in graph.coordinates.items():
        if coordinates == node_coordinates:
            return node_id, 0

        distance = calculate_distance(coordinates, node_coordinates)

        if distance < nearest_distance:
            nearest_node = node_id
            nearest_distance = distance

    if nearest_node is None or nearest_distance > max_distance:
        raise ValueError(
            "No road-network node found within "
            f"{max_distance} metres of this location."
        )

    return nearest_node, nearest_distance


def resolve_selection(graph, result, max_distance=1000):
    """Resolve a selected search result to a routable graph node."""
    if result["kind"] == "place":
        return resolve_to_graph_node(
            graph,
            result["coordinates"],
            max_distance=max_distance,
        )

    if result["kind"] == "road":
        # A road can contain many graph nodes. Use its first node as a
        # simple initial implementation; a later UI can let users select
        # a point along the road.
        if not result["nodes"]:
            raise ValueError("This road has no routable graph nodes.")

        node_id = result["nodes"][0]
        return node_id, 0

    raise ValueError("Unknown location type.")
