import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
_openai_client = OpenAI(api_key=_api_key) if _api_key else None

class StandardRAG:
    def __init__(self, embed_model='all-MiniLM-L6-v2'):
        self.embedding_model = SentenceTransformer(embed_model)
        self.vector_index = None
        self.corpus_docs = []
        
    def build_index(self, documents):
        """
        Encodes the list of documents and builds a FAISS vector index.
        """
        if not documents:
            print("[!] Warning: Empty document list. Cannot build StandardRAG index.")
            return
            
        self.corpus_docs = documents
        raw_texts = [doc['text'] for doc in documents]
        
        print(f"[*] StandardRAG: Encoding {len(raw_texts)} documents...")
        text_embeddings = self.embedding_model.encode(raw_texts, show_progress_bar=True)
        
        # Apply L2 normalization for cosine similarity search
        faiss.normalize_L2(text_embeddings)
        
        vector_dim = text_embeddings.shape[1]
        # Inner Product search on L2-normalized vectors yields Cosine Similarity
        self.vector_index = faiss.IndexFlatIP(vector_dim)
        self.vector_index.add(text_embeddings)
        print("[*] StandardRAG: FAISS index constructed successfully.")
        
    def query_index(self, question_text, top_n=3):
        """
        Finds the top_n most semantically similar documents in the index.
        """
        if self.vector_index is None:
            return []
            
        query_emb = self.embedding_model.encode([question_text])
        faiss.normalize_L2(query_emb)
        
        scores, match_indices = self.vector_index.search(query_emb, top_n)
        
        retrieved_contexts = []
        for idx in match_indices[0]:
            if idx != -1 and idx < len(self.corpus_docs):
                retrieved_contexts.append(self.corpus_docs[idx]['text'])
        return retrieved_contexts

    def generate_response(self, question_text):
        """
        Retrieves context and invokes the OpenAI API to generate an answer.
        """
        if not _api_key:
            return "Configuration Error: OPENAI_API_KEY environment variable is not set."
            
        retrieved_texts = self.query_index(question_text)
        if not retrieved_texts:
            return "No matching context found in standard document index."
            
        context_block = "\n\n".join(retrieved_texts)
        # Prevent context length overflow by truncating if needed
        if len(context_block) > 8000:
            context_block = context_block[:8000] + "\n...[truncated due to token limit]"
            
        system_instruction = f"""
        You are a highly knowledgeable technical assistant.
        Provide a concise and accurate response to the user's question, relying mainly on the provided context.
        If the context is insufficient, state this clearly, but you may use external knowledge to supplement the reply while prioritizing the context.
        
        Context material:
        {context_block}
        
        Question: {question_text}
        """
        
        try:
            completion = _openai_client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "user", "content": system_instruction}],
                temperature=0.1
            )
            return completion.choices[0].message.content.strip()
        except Exception as error:
            return f"Answer Generation Error: {error}"
