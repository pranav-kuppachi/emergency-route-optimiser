"""
Stores the road network as a graph and provides
methods to add locations and roads and retrieve
a location's neighbours.
"""

class RoadGraph: #Stores undirected road networks with non negative integers

    def __init__(self): #Initializing function
        self.adjacency_list = {} 

    def add_location(self, location): #Adds Location only if location hasn't been added.
        if location in self.adjacency_list:
             return
        self.adjacency_list[location] = [] #If location doesn't exist, we add it to dictionary with empty list as it's neighbours.

    def add_road(self, source, destination, distance, bidirectional = True): #Add road between 2 locations with distance
        self.add_location(source)
        self.add_location(destination)
        self.adjacency_list[source].append((destination, distance))
        if bidirectional: #Add the forward road. If the road is bidirectional, add the reverse road.
            self.adjacency_list[destination].append((source, distance))
        
    def neighbors(self, location): #Returns the list of neighboring locations and their road distances
        if location not in self.adjacency_list:
            raise KeyError("Location does not exist")
        return self.adjacency_list[location].copy() #Returns copy of the list instead of the original list itself, so we don't accidentally modify data

    def locations(self): #Returns all location IDs in our graph
        return list(self.adjacency_list)

    def __len__(self): #Returns total number of locations
        return len(self.adjacency_list)
    

    