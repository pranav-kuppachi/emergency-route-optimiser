
from ero.algorithms.shortest_path import (
    dijkstra_with_predecessors,
    reconstruct_path,
)
from ero.graph.osm_loader import load_road_graph
from ero.queues.radix_heap import RadixHeap


def main():
    graph = load_road_graph("data/coimbatore_roads.osm")

    # Nearest road nodes found from our landmark coordinates.
    start = 1228189707
    destination = 330044079

    distances, predecessors = dijkstra_with_predecessors(
        graph, start, RadixHeap()
    )

    path = reconstruct_path(predecessors, start, destination)

    print("\n=== Emergency Route Optimizer ===")
    print(f"Road-network locations: {len(graph):,}")

    if not path:
        print("No route found between the selected road nodes.")
        return

    print(f"Start node: {start}")
    print(f"Destination node: {destination}")
    print(f"Total road distance: {distances[destination]:,} metres")
    print(f"Road-network nodes in path: {len(path)}")

    print("\nPath:")
    print(" -> ".join(map(str, path)))


if __name__ == "__main__":
    main()
