import networkx as nx
import os
import json

def normalize_node(name):
    """
    Cleans up node names by trimming spaces and converting to title-case
    to prevent duplicate nodes with minor formatting variations.
    """
    if not isinstance(name, str):
        return ""
    stripped = name.strip()
    if stripped:
        # Standardize capitalization of the first letter
        stripped = stripped[0].upper() + stripped[1:]
    return stripped

def construct_kg(triples, save_path='outputs/graph.json'):
    """
    Constructs a directed knowledge graph from a list of triples using NetworkX.
    """
    graph = nx.DiGraph()
    
    for t in triples:
        subj = t.get('subject', '')
        obj = t.get('object', '')
        rel = t.get('relation', '')
        
        subj_normalized = normalize_node(subj)
        obj_normalized = normalize_node(obj)
        
        if subj_normalized and obj_normalized and rel:
            graph.add_edge(subj_normalized, obj_normalized, relation=rel.strip().lower())
            
    # Serialize the graph to JSON (node-link format)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    try:
        serialized_graph = nx.node_link_data(graph, edges="edges")
    except TypeError:
        serialized_graph = nx.node_link_data(graph)
        
    with open(save_path, 'w', encoding='utf-8') as f:
        json.dump(serialized_graph, f, indent=4, ensure_ascii=False)
        
    print(f"[*] Created Knowledge Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges.")
    return graph

def read_kg(load_path='outputs/graph.json'):
    """
    Loads and reconstructs a NetworkX graph from a node-link formatted JSON file.
    """
    if not os.path.exists(load_path):
        return None
    with open(load_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)
    try:
        return nx.node_link_graph(graph_data, edges="edges")
    except KeyError:
        return nx.node_link_graph(graph_data, edges="links")
    except TypeError:
        # Fallback if edges argument is not supported
        return nx.node_link_graph(graph_data)
