import networkx as nx
import matplotlib.pyplot as plt
import os

def plot_kg(graph, output_path='outputs/knowledge_graph.png', max_nodes=50):
    """
    Renders the knowledge graph using Matplotlib and saves the output plot.
    If the graph exceeds max_nodes, only visualizes the subgraph with high-degree nodes.
    """
    if graph is None or graph.number_of_nodes() == 0:
        print("[!] Graph is empty, skipping visualization.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Filter top nodes by degree if the graph contains too many elements
    if graph.number_of_nodes() > max_nodes:
        node_degrees = dict(graph.degree())
        top_nodes = sorted(node_degrees, key=node_degrees.get, reverse=True)[:max_nodes]
        display_subgraph = graph.subgraph(top_nodes)
        print(f"[*] Visualizing top {max_nodes} high-degree nodes (total: {graph.number_of_nodes()}).")
    else:
        display_subgraph = graph

    plt.figure(figsize=(14, 10))
    layouts = nx.spring_layout(display_subgraph, k=0.5, iterations=50)

    # Render nodes and node borders
    nx.draw_networkx_nodes(display_subgraph, layouts, node_size=2000, node_color='lightblue', alpha=0.9)
    
    # Render edges/relationships
    nx.draw_networkx_edges(display_subgraph, layouts, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=15)
    
    # Render labels for nodes
    nx.draw_networkx_labels(display_subgraph, layouts, font_size=10, font_weight='bold')

    # Render relation labels on edges
    relationship_labels = nx.get_edge_attributes(display_subgraph, 'relation')
    nx.draw_networkx_edge_labels(display_subgraph, layouts, edge_labels=relationship_labels, font_size=8, font_color='red')

    plt.title("Technology Sector Knowledge Graph Subgraph")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"[*] Graph visualization exported to: {output_path}")
