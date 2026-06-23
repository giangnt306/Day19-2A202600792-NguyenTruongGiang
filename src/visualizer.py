import networkx as nx
import matplotlib.pyplot as plt
import os

def visualize_graph(G, output_path='outputs/knowledge_graph.png', top_k=50):
    """
    Vẽ đồ thị và lưu ra file ảnh.
    Nếu đồ thị quá lớn, chỉ vẽ subgraph của top_k nodes có degree (bậc) cao nhất.
    """
    if G is None or G.number_of_nodes() == 0:
        print("[!] Graph is empty, nothing to visualize.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Lấy top K nodes nếu đồ thị quá lớn
    if G.number_of_nodes() > top_k:
        degrees = dict(G.degree())
        sorted_nodes = sorted(degrees, key=degrees.get, reverse=True)
        top_nodes = sorted_nodes[:top_k]
        H = G.subgraph(top_nodes)
        print(f"[*] Graph too large, visualizing top {top_k} nodes subgraph.")
    else:
        H = G

    plt.figure(figsize=(14, 10))
    pos = nx.spring_layout(H, k=0.5, iterations=50)

    # Draw nodes
    nx.draw_networkx_nodes(H, pos, node_size=2000, node_color='lightblue', alpha=0.9)
    
    # Draw edges
    nx.draw_networkx_edges(H, pos, edge_color='gray', arrows=True, arrowstyle='-|>', arrowsize=15)
    
    # Draw node labels
    nx.draw_networkx_labels(H, pos, font_size=10, font_weight='bold')

    # Draw edge labels
    edge_labels = nx.get_edge_attributes(H, 'relation')
    nx.draw_networkx_edge_labels(H, pos, edge_labels=edge_labels, font_size=8, font_color='red')

    plt.title("Tech Company Knowledge Graph")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    
    print(f"[*] Graph visualization saved to {output_path}")
