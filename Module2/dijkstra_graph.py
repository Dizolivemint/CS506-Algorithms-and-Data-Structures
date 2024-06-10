import heapq
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(graph, start):
    # Initialize distances from start to all nodes as infinity and set the start node distance to 0
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start] = 0
    
    # Priority queue to hold nodes to visit and their current known distances
    priority_queue = [(0, start)]  # (distance, node)
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        # Get the node with the smallest distance
        current_distance, current_node = heapq.heappop(priority_queue)
        print(f"Processing node: {current_node} with current distance: {current_distance}")
        
        # If the current distance is greater than the recorded shortest distance, skip this node
        if current_distance > shortest_distances[current_node]:
            continue
        
        # Explore neighbors of the current node
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            print(f"Checking neighbor: {neighbor} with edge weight: {weight}, "
                  f"current known distance: {shortest_distances[neighbor]}, "
                  f"new calculated distance: {distance}")
            
            # If a shorter path to neighbor is found, update the shortest distance and push to the queue
            if distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                print(f"Updated distance for node: {neighbor} to {distance}")
                print(f"Priority queue state: {priority_queue}")
    
    return shortest_distances, previous_nodes

def visualize_graph(graph, shortest_paths, start):
    G = nx.DiGraph()
    
    for node in graph:
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): f"{d['weight']}" for u, v, d in G.edges(data=True)}
    
    plt.figure(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=15, font_color='black', font_weight='bold')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12)
    
    shortest_path_edges = []
    for node, previous in shortest_paths.items():
        if previous is not None:
            shortest_path_edges.append((previous, node))
    
    nx.draw_networkx_edges(G, pos, edgelist=shortest_path_edges, edge_color='r', width=2)
    
    plt.title(f"Shortest Paths from Node {start}", size=20)
    plt.show()

# Example graph represented as an adjacency list
example_graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Running Dijkstra's Algorithm on the example graph from node 'A'
shortest_distances, previous_nodes = dijkstra(example_graph, 'A')
print("Final shortest paths:", shortest_distances)

# Visualize the graph and the shortest paths
visualize_graph(example_graph, previous_nodes, 'A')
