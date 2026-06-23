import pandas as pd
import os

def evaluate_systems(standard_rag_engine, graph_rag_engine, output_csv_path='outputs/evaluation.csv'):
    """
    Executes benchmark queries across both RAG configurations and exports results to a CSV report.
    """
    benchmark_queries = [
        "Công ty Apple có trụ sở ở đâu?",
        "Ai là CEO của Google?",
        "Bill Gates là người sáng lập công ty nào?",
        "Hệ điều hành Windows do ai phát triển?",
        "iPhone là sản phẩm của công ty nào?",
        "CEO hiện tại của Microsoft là ai?",
        "Alphabet Inc. sở hữu công ty nào?",
        "Google có trụ sở tại thành phố nào?",
        "Tim Cook làm việc ở vị trí nào tại Apple?",
        "Microsoft có phát triển hệ điều hành Mac không?",
        "Satya Nadella có mối quan hệ gì với Microsoft?",
        "Sundar Pichai có phải CEO của Apple không?",
        "Sản phẩm chủ lực của Apple là gì?",
        "Tập đoàn nào đứng sau công cụ tìm kiếm Google?",
        "Ai là người tạo ra Microsoft cùng với Paul Allen?",
        "Windows là sản phẩm cạnh tranh với hệ điều hành nào của Apple?",
        "Trụ sở Cupertino là của công ty nào?",
        "Ai là người điều hành cao nhất tại Alphabet Inc. hiện nay?",
        "Sản phẩm di động nổi tiếng nhất của Apple có tên là gì?",
        "Mountain View là nơi đặt trụ sở của công ty công nghệ nào?"
    ]
    
    evaluation_records = []
    print(f"[*] Starting evaluation of {len(benchmark_queries)} benchmark queries...")
    
    for idx, query in enumerate(benchmark_queries):
        print(f"  -> [{idx+1}/{len(benchmark_queries)}] Query: '{query}'")
        
        # Query Standard Vector RAG
        flat_reply = standard_rag_engine.generate_response(query) if standard_rag_engine else "StandardRAG not initialized"
        
        # Query Knowledge Graph RAG
        graph_reply = graph_rag_engine.generate_response(query) if graph_rag_engine else "KnowledgeRAG not initialized"
        
        evaluation_records.append({
            "question": query,
            "flat_rag_answer": flat_reply,
            "graph_rag_answer": graph_reply,
            "note": ""  # Left empty for custom analysis notes
        })
        
    dataframe = pd.DataFrame(evaluation_records)
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    dataframe.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"[*] Benchmark evaluation complete. Data saved to: {output_csv_path}")
