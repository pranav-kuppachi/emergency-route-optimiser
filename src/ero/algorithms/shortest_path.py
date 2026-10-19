
from ero.queues.interface import HeapInterface


def dijkstra_with_predecessors(graph, start, heap):
    locations = graph.locations()

    if start not in locations:
        raise KeyError("Starting location does not exist")

    distances = {location: float("inf") for location in locations}
    predecessors = {location: None for location in locations}

    distances[start] = 0
    heap.push(0, start)

    while not heap.is_empty():
        current_distance, current_location = heap.pop_min()

        if current_distance > distances[current_location]:
            continue

        for neighbor, road_distance in graph.neighbors(current_location):
            if road_distance < 0:
                raise ValueError("Road distances cannot be negative")

            new_distance = current_distance + road_distance

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_location
                heap.push(new_distance, neighbor)

    return distances, predecessors


def reconstruct_path(predecessors, start, destination):
    if start not in predecessors:
        raise KeyError("Starting location does not exist")

    if destination not in predecessors:
        raise KeyError("Destination location does not exist")

    if start == destination:
        return [start]

    path = []
    current = destination

    while current is not None:
        path.append(current)

        if current == start:
            path.reverse()
            return path

        current = predecessors[current]

    return []
