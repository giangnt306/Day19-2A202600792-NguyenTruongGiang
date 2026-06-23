import os
import sys

from src.flat_rag import FlatRAG
from src.graph_rag import GraphRAG
from src.data_loader import load_data, create_dummy_dataset
from src.entity_extractor import extract_all_documents
from src.graph_builder import build_knowledge_graph, load_knowledge_graph
from src.visualizer import visualize_graph
from src.evaluator import run_evaluation

def print_menu():
    print("\n" + "="*40)
    print("   LAB DAY 19: GRAPH RAG vs FLAT RAG")
    print("="*40)
    print("1. Build pipeline (Load data, Extract Triples, Build Graph, Index FlatRAG)")
    print("2. Ask with Flat RAG")
    print("3. Ask with GraphRAG")
    print("4. Run evaluation (20 benchmark questions)")
    print("5. Exit")
    print("="*40)

def main():
    flat_rag = None
    graph_rag = None
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            try:
                print("\n--- STEP 1: LOAD DATA ---")
                try:
                    docs = load_data()
                except FileNotFoundError:
                    print("[!] Dataset missing. Auto-creating dummy dataset for testing...")
                    create_dummy_dataset()
                    docs = load_data()
                    
                print("\n--- STEP 2: EXTRACT ENTITIES & RELATIONS ---")
                triples = extract_all_documents(docs)
                
                print("\n--- STEP 3: BUILD KNOWLEDGE GRAPH ---")
                G = build_knowledge_graph(triples)
                
                print("\n--- STEP 4: VISUALIZE GRAPH ---")
                visualize_graph(G)
                
                print("\n--- STEP 5: BUILD FLAT RAG INDEX ---")
                flat_rag = FlatRAG()
                flat_rag.build_index(docs)
                
                # Init GraphRAG
                graph_rag = GraphRAG(G)
                print("\n[*] PIPELINE BUILD SUCCESSFUL!")
                
            except Exception as e:
                print(f"[!] Pipeline Error: {e}")
                
        elif choice == '2':
            if not flat_rag:
                print("[!] Flat RAG is not initialized. Please run Build pipeline (1) first.")
                continue
            q = input("Enter question for Flat RAG: ")
            ans = flat_rag.answer(q)
            print(f"\n[Flat RAG Answer]:\n{ans}\n")
            
        elif choice == '3':
            if not graph_rag:
                print("[!] GraphRAG is not initialized. Please run Build pipeline (1) first.")
                continue
            q = input("Enter question for GraphRAG: ")
            ans = graph_rag.answer(q)
            print(f"\n[GraphRAG Answer]:\n{ans}\n")
            
        elif choice == '4':
            if not flat_rag or not graph_rag:
                print("[!] RAG systems not initialized. Run pipeline (1) first or loading from files is required.")
                print("[*] Automatically building pipeline to run evaluation...")
                # Try simple load
                try:
                    docs = load_data()
                    flat_rag = FlatRAG()
                    flat_rag.build_index(docs)
                    G = load_knowledge_graph()
                    if not G:
                        print("[!] Knowledge graph not found. Please run Option 1 first.")
                        continue
                    graph_rag = GraphRAG(G)
                except Exception as e:
                    print(f"Cannot auto-build: {e}")
                    continue
                    
            run_evaluation(flat_rag, graph_rag)
            
        elif choice == '5':
            print("Exiting...")
            sys.exit(0)
            
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
