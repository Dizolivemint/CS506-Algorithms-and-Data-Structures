import heapq
from typing import Dict, List, Tuple

class Graph:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes and their edges
        self.distances = {}  # Store actual distances in miles

    def add_edge(self, from_node: str, to_node: str, distance: float, speed: float):
        """
        Add an edge to the graph.
        :param from_node: Starting node
        :param to_node: Ending node
        :param distance: Distance in miles
        :param speed: Speed in mph
        """
        if from_node not in self.nodes:
            self.nodes[from_node] = {}
        weight = distance / speed  # Calculate weight as time (hours)
        self.nodes[from_node][to_node] = weight
        self.distances[(from_node, to_node)] = distance  # Store the actual distance
        if to_node not in self.nodes:
            self.nodes[to_node] = {}  # Ensure the destination node is in the graph, even if it has no outgoing edges

def dijkstra(graph: Graph, start: str, end: str) -> Tuple[List[str], float, float]:
    """
    Implement Dijkstra's algorithm to find the shortest path.
    :return: Tuple of (path, total_time, total_distance)
    """
    times = {node: float('infinity') for node in graph.nodes}
    times[start] = 0
    pq = [(0, start)]  # Priority queue: (time, node)
    previous_nodes = {}
    total_distance = 0

    while pq:
        current_time, current_node = heapq.heappop(pq)

        if current_node == end:
            # Reconstruct the path and calculate total distance
            path = []
            while current_node:
                path.append(current_node)
                if previous_nodes.get(current_node):
                    total_distance += graph.distances[(previous_nodes[current_node], current_node)]
                current_node = previous_nodes.get(current_node)
            return path[::-1], current_time, total_distance

        if current_time > times[current_node]:
            continue

        for neighbor, weight in graph.nodes[current_node].items():
            time = current_time + weight
            if time < times[neighbor]:
                times[neighbor] = time
                previous_nodes[neighbor] = current_node
                heapq.heappush(pq, (time, neighbor))

    return [], float('infinity'), float('infinity')

def update_traffic_data(graph: Graph, traffic_updates: Dict[Tuple[str, str], float]):
    """
    Update the graph with new traffic data.
    :param traffic_updates: Dictionary of edges and their new speeds in mph
    """
    for (from_node, to_node), new_speed in traffic_updates.items():
        if from_node in graph.nodes and to_node in graph.nodes[from_node]:
            distance = graph.distances[(from_node, to_node)]
            graph.nodes[from_node][to_node] = distance / new_speed

def optimize_route(graph: Graph, start: str, end: str, traffic_updates: Dict[Tuple[str, str], float]) -> Tuple[List[str], float, float]:
    """
    Optimize the route based on current traffic conditions.
    :return: Tuple of (optimal_path, total_time, total_distance)
    """
    update_traffic_data(graph, traffic_updates)
    return dijkstra(graph, start, end)

def format_time(hours: float) -> str:
    """
    Convert time from hours to a string format of minutes and seconds.
    :param hours: Time in hours
    :return: Formatted string of time in minutes and seconds
    """
    total_seconds = int(hours * 3600)  # Convert hours to seconds
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes} minutes, {seconds} seconds"
  
def print_route(start: str, end: str, traffic_scenario: str, traffic_updates: Dict[Tuple[str, str], float], graph: Graph):
    """
    Print the optimal route for a given scenario.
    """
    optimal_path, total_time, total_distance = optimize_route(graph, start, end, traffic_updates)
    formatted_time = format_time(total_time)
    print(f"\nScenario: {traffic_scenario}")
    print(f"Traffic updates (new speeds in mph): {traffic_updates}")
    print(f"Optimal path from {start} to {end}: {' -> '.join(optimal_path)}")
    print(f"Total time: {formatted_time}")
    print(f"Total distance: {total_distance:.2f} miles")

if __name__ == "__main__":
    # Create the graph
    g = Graph()
    # Adding edges with distance (miles) and initial speed (mph)
    g.add_edge("A", "B", 2, 35)  # 2 miles, initial speed 35 mph
    g.add_edge("A", "C", 1.5, 35)  # 1.5 miles, initial speed 35 mph
    g.add_edge("B", "D", 4.5, 45)  # 4.5 miles, initial speed 45 mph
    g.add_edge("C", "D", 6, 55)  # 6 miles, initial speed 55 mph
    g.add_edge("C", "E", 2.5, 35)  # 2.5 miles, initial speed 35 mph
    g.add_edge("D", "E", 3, 30)  # 3 miles, initial speed 30 mph

    # Scenario 1: No traffic updates (baseline)
    print_route("A", "E", "Baseline - No traffic", {}, g)

    # Scenario 2: Traffic jam on C-E
    traffic_updates_1 = {
        ("C", "E"): 10,  # Speed reduced to 10 mph on the optimal path
    }
    print_route("A", "E", "Traffic jam on C-E", traffic_updates_1, g)

    # Scenario 3: Heavy traffic on A-C
    traffic_updates_2 = {
        ("A", "C"): 15,  # Speed reduced to 15 mph
    }
    print_route("A", "E", "Heavy traffic on A-C", traffic_updates_2, g)

    # Scenario 4: Fast route opened
    traffic_updates_3 = {
        ("A", "B"): 60,  # Speed increased to 60 mph
        ("B", "D"): 60,  # Speed increased to 60 mph
        ("D", "E"): 60,  # Speed increased to 60 mph
    }
    print_route("A", "E", "Fast route A-B-D-E opened", traffic_updates_3, g)