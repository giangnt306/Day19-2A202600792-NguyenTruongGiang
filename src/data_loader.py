import os
import zipfile
import glob

def load_data(data_dir='data'):
    """
    Kiểm tra và giải nén dataset.zip nếu có.
    Đọc tất cả các file .txt trong data/dataset/.
    """
    dataset_zip = os.path.join(data_dir, 'dataset.zip')
    dataset_dir = os.path.join(data_dir, 'dataset')
    
    # Tạo thư mục data nếu chưa có
    os.makedirs(data_dir, exist_ok=True)
    
    # Giải nén nếu file zip tồn tại và thư mục chưa có dữ liệu
    if os.path.exists(dataset_zip):
        print(f"[*] Found {dataset_zip}, extracting...")
        with zipfile.ZipFile(dataset_zip, 'r') as zip_ref:
            zip_ref.extractall(dataset_dir)
        print("[*] Extraction complete.")
    elif not os.path.exists(dataset_dir):
        # Không có zip, không có dir -> Lỗi
        raise FileNotFoundError(f"Cannot find dataset.zip or '{dataset_dir}' directory. Please add data.")

    # Đọc tất cả file .txt
    txt_files = glob.glob(os.path.join(dataset_dir, '*.txt'))
    
    if not txt_files:
        # Thử tìm sâu hơn 1 level nếu zip giải nén thành folder bên trong
        txt_files = glob.glob(os.path.join(dataset_dir, '**', '*.txt'), recursive=True)
        
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {dataset_dir}.")
        
    documents = []
    print(f"[*] Found {len(txt_files)} .txt files.")
    for file_path in txt_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    documents.append({
                        "id": os.path.basename(file_path),
                        "text": content
                    })
        except Exception as e:
            print(f"[!] Error reading {file_path}: {e}")
            
    return documents

# Dummy content generator for missing dataset scenario
def create_dummy_dataset(data_dir='data'):
    dataset_dir = os.path.join(data_dir, 'dataset')
    os.makedirs(dataset_dir, exist_ok=True)
    
    dummy_docs = {
        "doc1.txt": "Apple is a technology company headquartered in Cupertino. Tim Cook is the CEO of Apple. Apple produces the iPhone.",
        "doc2.txt": "Google is owned by Alphabet Inc. Google is headquartered in Mountain View. Sundar Pichai is the CEO of Google.",
        "doc3.txt": "Microsoft was founded by Bill Gates. Microsoft develops the Windows operating system. Satya Nadella is the CEO of Microsoft."
    }
    
    for filename, content in dummy_docs.items():
        with open(os.path.join(dataset_dir, filename), 'w', encoding='utf-8') as f:
            f.write(content)
    print(f"[*] Created {len(dummy_docs)} dummy text files in {dataset_dir} for testing.")
