import networkx as nx
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
_api_key = os.getenv("OPENAI_API_KEY")
_openai_client = OpenAI(api_key=_api_key) if _api_key else None

class KnowledgeRAG:
    def __init__(self, knowledge_graph):
        self.graph = knowledge_graph
        
    def get_entities_from_query(self, query_text):
        """
        Uses the LLM to identify main named entities (companies, systems, key people) from the query.
        """
        ner_prompt = f"""
        You are a specialized Named Entity Recognition (NER) agent.
        Identify and extract the names of technology companies, platforms, key figures, or products from the input question.
        Return ONLY the extracted entity names as a comma-separated list. Do not include any explanations, greetings, or formatting.
        
        Question: {query_text}
        """
        try:
            completion = _openai_client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "user", "content": ner_prompt}],
                temperature=0.1
            )
            parsed_entities = [item.strip() for item in completion.choices[0].message.content.split(',') if item.strip()]
            return parsed_entities
        except Exception:
            # Fallback parsing mechanism if API call fails
            terms = query_text.split()
            return [term for term in terms if len(term) > 3]

    def extract_subgraph_context(self, entities_list, search_hops=2):
        """
        Locates the matching starting nodes in the graph and extracts an N-hop neighborhood.
        Textualizes the retrieved sub-graph edges for prompt context.
        """
        if not self.graph:
            return ""
            
        all_nodes = list(self.graph.nodes)
        lowercase_node_map = {str(node).lower(): node for node in all_nodes}
        
        starting_nodes = set()
        for ent in entities_list:
            ent_lower = ent.lower()
            if ent_lower in lowercase_node_map:
                starting_nodes.add(lowercase_node_map[ent_lower])
            else:
                # Substring matching fallback
                for node_lower, original_node in lowercase_node_map.items():
                    if ent_lower in node_lower or node_lower in ent_lower:
                        starting_nodes.add(original_node)
                        
        if not starting_nodes:
            return ""
            
        context_nodes = set(starting_nodes)
        
        # Traverse graph for N-hops
        for _ in range(search_hops):
            neighbors = set()
            for node in context_nodes:
                if self.graph.has_node(node):
                    neighbors.update(self.graph.successors(node))
                    neighbors.update(self.graph.predecessors(node))
            context_nodes.update(neighbors)
            
        # Reconstruct relationships in the neighborhood as text
        relationship_facts = []
        subgraph = self.graph.subgraph(context_nodes)
        for u, v, attrs in subgraph.edges(data=True):
            relation_desc = attrs.get('relation', 'is associated with')
            relationship_facts.append(f"{u} {relation_desc} {v}.")
            
        return " ".join(relationship_facts)

    def generate_response(self, question_text):
        """
        Identifies key entities, retrieves relevant sub-graphs, and answers the query using the LLM.
        """
        if not _api_key:
            return "Configuration Error: OPENAI_API_KEY environment variable is not set."
            
        query_entities = self.get_entities_from_query(question_text)
        graph_context = self.extract_subgraph_context(query_entities, search_hops=2)
        
        if not graph_context:
            return "No matching entities found in the Knowledge Graph for this question."
            
        structured_prompt = f"""
        You are a technical knowledge assistant.
        Answer the following question relying mainly on the provided Knowledge Graph context.
        The context is formatted as entity-relation triples (Subject -> Relation -> Object).
        If the context lacks sufficient details, use your general knowledge to construct a complete answer but clearly indicate which details are external.
        
        Knowledge Graph context:
        {graph_context}
        
        Question: {question_text}
        """
        
        try:
            completion = _openai_client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{"role": "user", "content": structured_prompt}],
                temperature=0.1
            )
            return completion.choices[0].message.content.strip()
        except Exception as error:
            return f"Answer Generation Error: {error}"
