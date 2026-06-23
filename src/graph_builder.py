import networkx as nx
import os
import json

def clean_node(node_name):
    """
    Làm sạch tên node: loại bỏ khoảng trắng dư thừa, 
    viết hoa chữ cái đầu (để đơn giản deduplication).
    """
    if not isinstance(node_name, str):
        return ""
    cleaned = node_name.strip()
    # Simple capitalization for normalization
    if cleaned:
        cleaned = cleaned[0].upper() + cleaned[1:]
    return cleaned

def build_knowledge_graph(triples, output_path='outputs/graph.json'):
    """
    Xây dựng Knowledge Graph từ list triples bằng NetworkX.
    """
    G = nx.DiGraph()
    
    for t in triples:
        subj = t.get('subject', '')
        obj = t.get('object', '')
        rel = t.get('relation', '')
        
        # Deduplication đơn giản
        subj_clean = clean_node(subj)
        obj_clean = clean_node(obj)
        
        if subj_clean and obj_clean and rel:
            G.add_edge(subj_clean, obj_clean, relation=rel.strip().lower())
            
    # Lưu đồ thị dạng JSON (node-link format)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data = nx.node_link_data(G)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"[*] Built Knowledge Graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G

def load_knowledge_graph(path='outputs/graph.json'):
    """
    Load đồ thị từ file json.
    """
    if not os.path.exists(path):
        return None
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return nx.node_link_graph(data)
