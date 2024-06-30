import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph
G = nx.DiGraph()

# Add edges and their weights
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

G.add_weighted_edges_from(edges)

# Draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold')
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_weight='bold')

plt.title("Graph for Bellman-Ford Algorithm")
plt.show()
