import heapq
from typing import Dict, List, Tuple

# Define a class to represent the graph
class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store adjacency list of nodes

    # Method to add edges to the graph
    def add_edge(self, from_node: str, to_node: str, weight: int):
        if from_node not in self.nodes:
            self.nodes[from_node] = {}  # Initialize an empty adjacency list for the node
        self.nodes[from_node][to_node] = weight  # Add the edge with its weight
        if to_node not in self.nodes:
          self.nodes[to_node] = {} # Ensure the destination node is in the graph, even if it has no outgoing edges

# Function to perform Dijkstra's algorithm
def dijkstra(graph: Graph, start: str, end: str) -> Tuple[List[str], int]:
    distances = {node: float('infinity') for node in graph.nodes}  # Initialize distances to infinity
    distances[start] = 0  # Distance to the start node is 0
    pq = [(0, start)]  # Priority queue to select the node with the smallest distance
    previous_nodes = {}  # Dictionary to store the path

    while pq:
        current_distance, current_node = heapq.heappop(pq)  # Get the node with the smallest distance

        if current_node == end:  # If we reach the end node, reconstruct the path
            path = []
            while current_node:
                path.append(current_node)
                current_node = previous_nodes.get(current_node)
            return path[::-1], current_distance  # Return the reversed path and the total distance

        if current_distance > distances[current_node]:
            continue  # Skip processing if a better path is already found

        for neighbor, weight in graph.nodes[current_node].items():
            distance = current_distance + weight  # Calculate the new distance
            if distance < distances[neighbor]:  # If a shorter path is found
                distances[neighbor] = distance  # Update the distance
                previous_nodes[neighbor] = current_node  # Update the path
                heapq.heappush(pq, (distance, neighbor))  # Push the new distance to the priority queue

    return [], float('infinity')  # Return empty path and infinity if no path is found

# Function to update the graph with real-time traffic data
def update_traffic_data(graph: Graph, traffic_updates: Dict[Tuple[str, str], int]):
    for (from_node, to_node), new_weight in traffic_updates.items():
        if from_node in graph.nodes and to_node in graph.nodes[from_node]:
            graph.nodes[from_node][to_node] = new_weight  # Update the edge weight with new traffic data

# Function to optimize the route considering real-time traffic updates
def optimize_route(graph: Graph, start: str, end: str, traffic_updates: Dict[Tuple[str, str], int]) -> Tuple[List[str], int]:
    update_traffic_data(graph, traffic_updates)  # Update the graph with real-time traffic data
    return dijkstra(graph, start, end)  # Perform Dijkstra's algorithm to find the optimal path

def print_route(start: str, end: str, traffic_scenario: str, traffic_updates: Dict[Tuple[str, str], int], graph: Graph):
    optimal_path, total_distance = optimize_route(graph, start, end, traffic_updates)
    print(f"\nScenario: {traffic_scenario}")
    print(f"Traffic updates: {traffic_updates}")
    print(f"Optimal path from {start} to {end}: {' -> '.join(optimal_path)}")
    print(f"Total distance: {total_distance}")

if __name__ == "__main__":
    # Create the initial graph
    g = Graph()
    
    # Example route plan
    g.add_edge("A", "B", 4)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "D", 3)
    g.add_edge("C", "D", 1)
    g.add_edge("C", "E", 5)
    g.add_edge("D", "E", 2)

    # Scenario: No traffic updates (baseline)
    print_route("A", "E", "Baseline - No traffic", {}, g)

    # Scenario: Decrease traffic on A-B and increase on C-D
    traffic_updates_1 = {
        ("A", "B"): 1,  # Decrease traffic on edge A-B
        ("C", "D"): 3,  # Slight increase in traffic on edge C-D
    }
    print_route("A", "E", "Decrease traffic on A-B and increase on C-D", traffic_updates_1, g)

    # Scenario: Heavy traffic on C-D
    traffic_updates_2 = {
        ("C", "D"): 5,  # Heavy traffic on edge C-D
    }
    print_route("A", "E", "Heavy traffic on C-D", traffic_updates_2, g)

    # Scenario: Multiple route changes
    traffic_updates_4 = {
        ("A", "B"): 1,  # A-B becomes very fast
        ("B", "D"): 1,  # B-D becomes very fast
        ("C", "D"): 6,  # C-D becomes slow
        ("C", "E"): 10, # C-E becomes very slow
    }
    print_route("A", "E", "Multiple route changes", traffic_updates_4, g)
