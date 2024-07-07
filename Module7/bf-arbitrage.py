import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

def bellman_ford(graph, source):
    # Step 1: Initialize distances
    distance = {node: float('inf') for node in graph.nodes}
    distance[source] = 0
    previous = {node: None for node in graph.nodes}

    # Step 2: Relax edges (V-1) times
    for _ in range(len(graph.nodes) - 1):
        for u, v, w in graph.edges(data='weight'):
            if distance[u] + w < distance[v]:
                distance[v] = distance[u] + w
                previous[v] = u

    # Step 3: Check for negative-weight cycles
    for u, v, w in graph.edges(data='weight'):
        if distance[u] + w < distance[v]:
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
    ('USD', 'EUR', -np.log(0.95)),
    ('EUR', 'GBP', -np.log(0.75)),
    ('GBP', 'USD', -np.log(2))
]

# Create the graph
G = nx.DiGraph()
G.add_weighted_edges_from(edges)

# Run Bellman-Ford algorithm to detect negative-weight cycle
source_node = 'USD'
negative_cycle = bellman_ford(G, source_node)

if negative_cycle:
    print("Arbitrage opportunity detected in the cycle:", negative_cycle)
else:
    print("No arbitrage opportunity detected.")

# Display the graph
pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, 'weight')
labels = {k: f"{np.exp(-v):.2f}" for k, v in labels.items()}  # Convert weights back to exchange rates for display
plt.figure(figsize=(10, 7))
nx.draw(G, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=12, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
plt.title("Currency Exchange Graph")
plt.show()
