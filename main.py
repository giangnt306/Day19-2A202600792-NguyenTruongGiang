import os
import sys

from src.rag_flat import StandardRAG
from src.rag_graph import KnowledgeRAG
from src.loader import read_corpus, generate_test_dataset
from src.extractor import process_corpus
from src.builder import construct_kg, read_kg
from src.plot import plot_kg
from src.evaluation import evaluate_systems

def show_options():
    print("\n" + "="*45)
    print("      LAB WORK: KNOWLEDGE GRAPH RAG COMPARISON")
    print("="*45)
    print("1. Build and Run Pipeline (Extract Triples, KG, Flat Index)")
    print("2. Retrieve and Answer using Flat Vector RAG")
    print("3. Retrieve and Answer using Knowledge Graph RAG")
    print("4. Perform Benchmark Evaluation (20-Question Set)")
    print("5. Exit Program")
    print("="*45)

def main():
    standard_rag = None
    knowledge_rag = None
    
    while True:
        show_options()
        user_choice = input("Select an option (1-5): ").strip()
        
        if user_choice == '1':
            try:
                print("\n--- STAGE 1: LOADING RAW CORPUS ---")
                try:
                    documents = read_corpus()
                except FileNotFoundError:
                    print("[!] Corpus not found. Auto-generating test sample data...")
                    generate_test_dataset()
                    documents = read_corpus()
                    
                print("\n--- STAGE 2: EXTRACTING RELATION TRIPLES ---")
                triples = process_corpus(documents)
                
                print("\n--- STAGE 3: CONSTRUCTING KNOWLEDGE GRAPH ---")
                kg_graph = construct_kg(triples)
                
                print("\n--- STAGE 4: EXPORTING GRAPH VISUALIZATION ---")
                plot_kg(kg_graph)
                
                print("\n--- STAGE 5: INDEXING FLAT VECTOR RAG ---")
                standard_rag = StandardRAG()
                standard_rag.build_index(documents)
                
                # Instantiate Knowledge Graph RAG
                knowledge_rag = KnowledgeRAG(kg_graph)
                print("\n[*] PIPELINE REBUILT SUCCESSFULLY!")
                
            except Exception as err:
                print(f"[!] Pipeline Execution Error: {err}")
                
        elif user_choice == '2':
            if not standard_rag:
                print("[!] Standard RAG is not initialized. Please build the pipeline (1) first.")
                continue
            question = input("Enter query for Standard RAG: ")
            reply = standard_rag.generate_response(question)
            print(f"\n[Standard RAG Response]:\n{reply}\n")
            
        elif user_choice == '3':
            if not knowledge_rag:
                print("[!] Knowledge Graph RAG is not initialized. Please build the pipeline (1) first.")
                continue
            question = input("Enter query for Knowledge Graph RAG: ")
            reply = knowledge_rag.generate_response(question)
            print(f"\n[Knowledge Graph RAG Response]:\n{reply}\n")
            
        elif user_choice == '4':
            if not standard_rag or not knowledge_rag:
                print("[!] RAG systems not fully loaded. Attempting automatic build from cached files...")
                try:
                    documents = read_corpus()
                    standard_rag = StandardRAG()
                    standard_rag.build_index(documents)
                    kg_graph = read_kg()
                    if not kg_graph:
                        print("[!] Knowledge graph cache missing. Please run option 1 first.")
                        continue
                    knowledge_rag = KnowledgeRAG(kg_graph)
                except Exception as err:
                    print(f"[!] Auto-initialization failed: {err}")
                    continue
                    
            evaluate_systems(standard_rag, knowledge_rag)
            
        elif user_choice == '5':
            print("Exiting application...")
            sys.exit(0)
            
        else:
            print("Selection invalid. Please choose from 1 to 5.")

if __name__ == "__main__":
    main()
