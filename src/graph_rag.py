import networkx as nx
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

class GraphRAG:
    def __init__(self, graph):
        self.G = graph
        
    def extract_main_entities(self, question):
        """
        Dùng Gemini để trích xuất danh sách các entities chính từ câu hỏi.
        """
        prompt = f"""
        Bạn là một NER (Named Entity Recognition) model.
        Hãy trích xuất tên của các công ty công nghệ, nhân vật, sản phẩm từ câu hỏi sau.
        Chỉ trả về các thực thể phân cách bằng dấu phẩy, không có text giải thích.
        
        Câu hỏi: {question}
        """
        try:
            response = client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            entities = [e.strip() for e in response.choices[0].message.content.split(',')]
            return entities
        except:
            # Fallback simple keyword match
            words = question.split()
            return [w for w in words if len(w) > 3]

    def get_context_from_graph(self, entities, hop=2):
        """
        Tìm các node liên quan và lấy 2-hop neighbors.
        Textualize graph thành dạng string.
        """
        if not self.G:
            return ""
            
        nodes_in_graph = list(self.G.nodes)
        lower_nodes = {str(n).lower(): n for n in nodes_in_graph}
        
        matched_nodes = set()
        for e in entities:
            e_lower = e.lower()
            # Exact match (case insensitive)
            if e_lower in lower_nodes:
                matched_nodes.add(lower_nodes[e_lower])
            else:
                # Substring match
                for node_lower, orig_node in lower_nodes.items():
                    if e_lower in node_lower or node_lower in e_lower:
                        matched_nodes.add(orig_node)
                        
        if not matched_nodes:
            return ""
            
        subgraph_nodes = set(matched_nodes)
        
        # Traverse 2-hop
        for _ in range(hop):
            current_neighbors = set()
            for node in subgraph_nodes:
                if self.G.has_node(node):
                    current_neighbors.update(self.G.successors(node))
                    current_neighbors.update(self.G.predecessors(node))
            subgraph_nodes.update(current_neighbors)
            
        # Textualize edges
        context_sentences = []
        subG = self.G.subgraph(subgraph_nodes)
        for u, v, data in subG.edges(data=True):
            rel = data.get('relation', 'related to')
            context_sentences.append(f"{u} {rel} {v}.")
            
        return " ".join(context_sentences)

    def answer(self, question):
        if not OPENAI_API_KEY:
            return "Error: OPENAI_API_KEY not found."
            
        entities = self.extract_main_entities(question)
        context_text = self.get_context_from_graph(entities, hop=2)
        
        if not context_text:
            return "Không tìm thấy entity nào trong Knowledge Graph khớp với câu hỏi."
            
        prompt = f"""
        Bạn là một trợ lý ảo am hiểu về công nghệ.
        Hãy trả lời câu hỏi sau dựa MỘT PHẦN VÀO ngữ cảnh đồ thị tri thức (Knowledge Graph) được cung cấp.
        Ngữ cảnh là các chuỗi quan hệ (Subject -> Relation -> Object).
        Nếu ngữ cảnh không chứa đủ thông tin, hãy dùng kiến thức của bạn để bổ sung nhưng ưu tiên ngữ cảnh.
        
        Ngữ cảnh từ Graph:
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
