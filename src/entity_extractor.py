import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load env variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

def extract_triples_from_text(text, model_name='gpt-4o-mini'):
    """
    Gọi OpenAI API để trích xuất list các triples: subject, relation, object.
    """
    if not OPENAI_API_KEY:
        print("[!] Warning: OPENAI_API_KEY is not set.")
        return []
        
    prompt = f"""
    Bạn là một chuyên gia trích xuất thực thể và mối quan hệ (Information Extraction).
    Hãy đọc đoạn văn bản sau và trích xuất tất cả các mối quan hệ (triples) dưới dạng JSON array.
    Mỗi phần tử trong array là một object có 3 khóa: "subject", "relation", "object".
    Chỉ trả về JSON hợp lệ, không bọc trong markdown code block, không thêm text giải thích.
    
    Ví dụ:
    [
      {{"subject": "Apple", "relation": "headquartered in", "object": "Cupertino"}},
      {{"subject": "Tim Cook", "relation": "CEO of", "object": "Apple"}}
    ]

    Văn bản:
    {text}
    """
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1
        )
        content = response.choices[0].message.content.strip()
        
        # Làm sạch kết quả nếu model có trả về markdown (VD: ```json ... ```)
        if content.startswith("```json"):
            content = content[7:]
        if content.startswith("```"):
            content = content[3:]
        if content.endswith("```"):
            content = content[:-3]
            
        content = content.strip()
        
        # Parse JSON
        triples = json.loads(content)
        if isinstance(triples, list):
            return triples
        return []
        
    except json.JSONDecodeError:
        print("[!] JSONDecodeError: Gemini return invalid JSON.")
        print(f"Raw output: {content[:100]}...")
        return []
    except Exception as e:
        print(f"[!] Exception during OpenAI API call: {e}")
        return []

def extract_all_documents(documents, output_path='outputs/triples.json'):
    """
    Trích xuất toàn bộ triples từ list documents. Lưu cache để tránh gọi lại API.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Load cache if exists
    if os.path.exists(output_path):
        print(f"[*] Loading cached triples from {output_path}")
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    all_triples = []
    print(f"[*] Extracting triples for {len(documents)} documents using OpenAI API...")
    
    for i, doc in enumerate(documents):
        print(f"    -> Processing doc {i+1}/{len(documents)}: {doc['id']}")
        triples = extract_triples_from_text(doc['text'])
        # Thêm source để traceback
        for t in triples:
            t['source_doc'] = doc['id']
        all_triples.extend(triples)
        
    # Save cache
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_triples, f, indent=4, ensure_ascii=False)
        
    print(f"[*] Saved {len(all_triples)} triples to {output_path}")
    return all_triples
