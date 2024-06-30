import networkx as nx
import pandas as pd

def bellman_ford(graph, source):
    # Step 1: Initialize distances
    distance = {node: float('inf') for node in graph.nodes}
    distance[source] = 0
    print("Initial distances:", distance)

    # Step 2: Relax edges (V-1) times
    for i in range(len(graph.nodes) - 1):
        print(f"\nIteration {i + 1}")
        for u, v, w in graph.edges(data='weight'):
            if distance[u] != float('inf') and distance[u] + w < distance[v]:
                print(f"Relaxing edge ({u} -> {v}) with weight {w}")
                print(f"Distance to {v} updated from {distance[v]} to {distance[u] + w}")
                distance[v] = distance[u] + w
        print("Distances after this iteration:", distance)

    # Step 3: Check for negative-weight cycles
    negative_cycle_detected = False
    for u, v, w in graph.edges(data='weight'):
        if distance[u] != float('inf') and distance[u] + w < distance[v]:
            print(f"Negative-weight cycle detected: edge ({u} -> {v}) with weight {w}")
            negative_cycle_detected = True
            break

    if negative_cycle_detected:
        print("Graph contains a negative-weight cycle. Shortest paths calculated up to detection:")
    else:
        print("No negative-weight cycles detected. Final shortest paths:")

    return distance

# Define the edges and their weights
edges = [
    ('A', 'B', 4),
    ('A', 'C', 2),
    ('B', 'C', 3),
    ('B', 'D', 2),
    ('C', 'B', 1),
    ('C', 'D', 4),
    ('D', 'E', 2),
    ('E', 'A', -10)
]

# Create the graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Run Bellman-Ford algorithm
source_node = 'A'
distances = bellman_ford(G, source_node)

# Display the shortest distances
distances_df = pd.DataFrame(list(distances.items()), columns=['Vertex', 'Distance'])
print(distances_df)
