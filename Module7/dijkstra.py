import networkx as nx
import matplotlib.pyplot as plt
import heapq

def dijkstra(graph, source):
    # Step 1: Initialize distances and priority queue
    distance = {node: float('inf') for node in graph.nodes}
    previous = {node: None for node in graph.nodes}
    distance[source] = 0
    priority_queue = [(0, source)]
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_distance > distance[current_node]:
            continue
        
        for neighbor, weight in graph[current_node].items():
            distance_through_current = current_distance + weight['weight']
            if distance_through_current < distance[neighbor]:
                distance[neighbor] = distance_through_current
                previous[neighbor] = current_node
                heapq.heappush(priority_queue, (distance_through_current, neighbor))
    
    return distance, previous

def reconstruct_path(previous, source, target):
    path = []
    current = target
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path

def draw_graph(graph, source, target, path):
    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 7))
    
    # Draw the entire graph
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=10)
    
    # Highlight the shortest path
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_color='lightgreen', node_size=700)
    nx.draw_networkx_edges(graph, pos, edgelist=path_edges, edge_color='red', width=2)
    
    plt.title(f"Shortest path from {source} to {target}")
    plt.show()

# Define the edges and their weights
edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 1),
    ('B', 'D', 5),
    ('C', 'D', 8),
    ('C', 'E', 10),
    ('D', 'E', 2),
    ('D', 'Z', 6),
    ('E', 'Z', 3)
]

# Create the graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Run Dijkstra's algorithm
source_node = 'A'
target_node = 'Z'
distances, previous = dijkstra(G, source_node)

# Reconstruct the shortest path
shortest_path = reconstruct_path(previous, source_node, target_node)

# Draw the graph with the shortest path highlighted
draw_graph(G, source_node, target_node, shortest_path)

# Display the shortest distances
distances_df = pd.DataFrame(list(distances.items()), columns=['Vertex', 'Distance'])
print(distances_df)
