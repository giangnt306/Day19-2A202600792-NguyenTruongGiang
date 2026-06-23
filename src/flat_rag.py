import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class FlatRAG:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.encoder = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        
    def build_index(self, docs):
        """
        docs: list of dict {'id': ..., 'text': ...}
        """
        if not docs:
            print("[!] No documents to index for Flat RAG.")
            return
            
        self.documents = docs
        texts = [doc['text'] for doc in docs]
        
        print(f"[*] Encoding {len(texts)} documents for Flat RAG...")
        embeddings = self.encoder.encode(texts, show_progress_bar=True)
        
        # L2 norm for cosine similarity
        faiss.normalize_L2(embeddings)
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dimension) # Inner Product -> Cosine Sim because normalized
        self.index.add(embeddings)
        print("[*] Flat RAG Index built successfully.")
        
    def retrieve(self, question, top_k=3):
        if self.index is None:
            return []
            
        q_emb = self.encoder.encode([question])
        faiss.normalize_L2(q_emb)
        
        distances, indices = self.index.search(q_emb, top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.documents):
                results.append(self.documents[idx]['text'])
        return results

    def answer(self, question):
        if not OPENAI_API_KEY:
            return "Error: OPENAI_API_KEY not found."
            
        contexts = self.retrieve(question)
        if not contexts:
            return "Không tìm thấy thông tin ngữ cảnh nào."
            
        context_text = "\n\n".join(contexts)
        # Giới hạn độ dài context để không bị lỗi 400 (context_length_exceeded)
        if len(context_text) > 8000:
            context_text = context_text[:8000] + "\n...[truncated]"
        prompt = f"""
        Bạn là một trợ lý ảo am hiểu về công nghệ.
        Hãy trả lời câu hỏi sau dựa MỘT PHẦN VÀO ngữ cảnh được cung cấp.
        Nếu ngữ cảnh không chứa đủ thông tin, hãy nói rõ, hoặc dùng kiến thức của bạn nhưng ưu tiên ngữ cảnh.
        
        Ngữ cảnh:
        {context_text}
        
        Câu hỏi: {question}
        """
        
        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generation answer: {e}"
