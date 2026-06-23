import os
import zipfile
import glob

def read_corpus(folder_path='data'):
    """
    Checks for the existence of dataset.zip and extracts it if present.
    Loads and reads all text files located inside data/dataset/ directory.
    """
    archive_file = os.path.join(folder_path, 'dataset.zip')
    extract_target = os.path.join(folder_path, 'dataset')
    
    os.makedirs(folder_path, exist_ok=True)
    
    # Auto-extract zip file if available and target directory is missing
    if os.path.exists(archive_file):
        print(f"[*] Extracting archive: {archive_file}...")
        with zipfile.ZipFile(archive_file, 'r') as zip_ref:
            zip_ref.extractall(extract_target)
        print("[*] Extraction complete.")
    elif not os.path.exists(extract_target):
        raise FileNotFoundError(f"Missing data: Place 'dataset.zip' or create '{extract_target}' directory.")

    # Retrieve all text documents
    text_paths = glob.glob(os.path.join(extract_target, '*.txt'))
    
    # If empty, check recursively for nested directory structures
    if not text_paths:
        text_paths = glob.glob(os.path.join(extract_target, '**', '*.txt'), recursive=True)
        
    if not text_paths:
        raise FileNotFoundError(f"No text files found in the dataset directory '{extract_target}'.")
        
    docs_list = []
    print(f"[*] Found {len(text_paths)} text files to process.")
    for path in text_paths:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                body = f.read().strip()
                if body:
                    docs_list.append({
                        "id": os.path.basename(path),
                        "text": body
                    })
        except Exception as err:
            print(f"[!] Failed to read file {path}: {err}")
            
    return docs_list


def generate_test_dataset(folder_path='data'):
    """
    Generates a tiny dummy dataset for development/testing when no actual data is present.
    """
    target_dir = os.path.join(folder_path, 'dataset')
    os.makedirs(target_dir, exist_ok=True)
    
    sample_data = {
        "doc1.txt": "Apple is a technology company headquartered in Cupertino. Tim Cook is the CEO of Apple. Apple produces the iPhone.",
        "doc2.txt": "Google is owned by Alphabet Inc. Google is headquartered in Mountain View. Sundar Pichai is the CEO of Google.",
        "doc3.txt": "Microsoft was founded by Bill Gates. Microsoft develops the Windows operating system. Satya Nadella is the CEO of Microsoft."
    }
    
    for fname, body in sample_data.items():
        with open(os.path.join(target_dir, fname), 'w', encoding='utf-8') as f:
            f.write(body)
    print(f"[*] Generated dummy dataset containing {len(sample_data)} files in '{target_dir}'.")
