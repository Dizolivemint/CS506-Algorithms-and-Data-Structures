import networkx as nx
import matplotlib.pyplot as plt

def bellman_ford(graph, source):
    # Step 1: Initialize distances
    distance = {node: float('inf') for node in graph.nodes}
    distance[source] = 0
    previous = {node: None for node in graph.nodes}

    # Step 2: Relax edges (V-1) times
    for _ in range(len(graph.nodes) - 1):
        for u, v, w in graph.edges(data='weight'):
            if distance[u] != float('inf') and distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                previous[v] = u

    # Step 3: Check for negative-weight cycles
    for u, v, w in graph.edges(data='weight'):
        if distance[u] != float('inf') and distance[u] + w < distance[v]:
            # Negative cycle detected
            cycle = []
            current = v
            while current not in cycle:
                cycle.append(current)
                current = previous[current]
            cycle.append(current)
            cycle = cycle[cycle.index(current):]  # Truncate cycle to start from the first repeated node
            cycle.reverse()
            return cycle

    return None

# Define the edges and their weights
edges = [
    ('A', 'B', 3),
    ('B', 'C', -2),
    ('C', 'D', 2),
    ('D', 'E', -1),
    ('E', 'A', 5)
]

# Create the graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Run Bellman-Ford algorithm to detect negative-weight cycle
source_node = 'A'
negative_cycle = bellman_ford(G, source_node)

if negative_cycle:
    print("Performance improvement loop detected in the cycle:", negative_cycle)
else:
    print("No performance improvement loop detected.")

# Display the graph
pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, 'weight')
plt.figure(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
plt.title("Football Performance Metrics Graph")
plt.show()
