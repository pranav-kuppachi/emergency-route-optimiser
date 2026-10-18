'''
Implements Dijkstra's shortest-path algorithm.
The algorithm works with any heap that follows HeapInterface to compare
Binomial, Leftist, Radix, and Skew Heaps without changing the shortest-path algorithm.
'''

from ero.queues.interface import HeapInterface

def dijkstra(graph, start, heap):
    locations = graph.locations()
    if start not in locations:
        raise KeyError("Starting location does not exist")
    distances = {}
    for location in locations:
       distances[location] = float("inf")

    distances[start] = 0 # The distance from the starting location to itself is 0
    heap.push(0, start) #begin by inserting the starting loc into heap

    while not heap.is_empty():
        current_distance, current_location = heap.pop_min()# Remove the location with the smallest recorded priority.
        if current_distance > distances[current_location]:
            continue # A shorter route to this location may have been found earlier.

        for neighbor, road_distance in graph.neighbors(current_location): # Examine every road leaving the current location.
            if road_distance < 0:  
                raise ValueError("Road distances cannot be negative")
            
            new_distance = current_distance + road_distance  # Calculate the distance to the neighbor through this road.

            if new_distance < distances[neighbor]: # If this route is shorter, update the best known distance.
                distances[neighbor] = new_distance
                heap.push(new_distance, neighbor) # Insert the improved route into the heap.

    return distances



