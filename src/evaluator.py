import pandas as pd
import os

def run_evaluation(flat_rag, graph_rag, output_path='outputs/evaluation.csv'):
    """
    Chạy 20 câu hỏi benchmark và lưu kết quả ra file csv.
    """
    questions = [
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
    
    results = []
    print(f"[*] Running evaluation on {len(questions)} benchmark questions...")
    
    for i, q in enumerate(questions):
        print(f"  -> Q{i+1}: {q}")
        
        # Flat RAG
        flat_ans = flat_rag.answer(q) if flat_rag else "FlatRAG Not Initialized"
        
        # Graph RAG
        graph_ans = graph_rag.answer(q) if graph_rag else "GraphRAG Not Initialized"
        
        results.append({
            "question": q,
            "flat_rag_answer": flat_ans,
            "graph_rag_answer": graph_ans,
            "note": "" # Cột trống cho user điền
        })
        
    df = pd.DataFrame(results)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"[*] Evaluation completed. Results saved to {output_path}")
