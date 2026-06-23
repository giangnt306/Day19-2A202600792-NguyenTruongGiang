# Thực nghiệm Lab Day 19: Nghiên cứu So sánh giữa GraphRAG và Flat RAG trên dữ liệu Doanh nghiệp Công nghệ

Hệ thống Retrieval-Augmented Generation (RAG) này được thiết lập nhằm phân tích, đánh giá và đối chiếu hiệu quả truy xuất thông tin giữa hai kỹ thuật phổ biến:
1. **Flat RAG (RAG truyền thống)**: Ứng dụng Cơ sở dữ liệu Vector (`faiss-cpu`) kết hợp mô hình trích xuất đặc trưng (`sentence-transformers`) để truy vấn các đoạn văn bản tương đồng.
2. **GraphRAG (RAG trên Đồ thị)**: Thiết lập Đồ thị Tri thức (Knowledge Graph) từ ngữ liệu thô (sử dụng Gemini API để trích xuất và thư viện `networkx` để kiến thiết đồ thị), sau đó thực hiện tìm kiếm và mở rộng ngữ cảnh qua các liên kết láng giềng trong phạm vi 2-hop.

## Cấu trúc thư mục

```text
.
├── .env                    # Tệp lưu cấu hình khóa API (OPENAI_API_KEY)
├── .env.example            # Tệp cấu hình mẫu
├── main.py                 # Tệp khởi chạy chính của chương trình
├── README.md               # Tài liệu hướng dẫn chi tiết
├── requirements.txt        # Danh sách các thư viện Python cần cài đặt
├── data/
│   └── dataset/            # Thư mục lưu trữ tập dữ liệu corpus dạng văn bản (.txt)
├── outputs/                # Thư mục tự động xuất kết quả thực nghiệm
│   ├── analysis.md         # Phân tích tổng quan chi phí thời gian và API Token
│   ├── evaluation.csv      # Bảng kết quả benchmark 20 câu hỏi (dạng CSV)
│   ├── evaluation.md       # Bảng đánh giá và đối chiếu kết quả (dạng Markdown)
│   ├── graph.json          # Cấu trúc đồ thị tri thức dưới dạng Node-Link JSON
│   ├── knowledge_graph.png # Biểu đồ trực quan hóa đồ thị tri thức (Top 50 nodes)
│   └── triples.json        # Bản lưu cache các quan hệ (Subject - Relation - Object)
├── src/
│   ├── data_loader.py      # Bộ nạp và tiền xử lý dữ liệu đầu vào
│   ├── entity_extractor.py # Module phân tách thực thể và quan hệ từ văn bản
│   ├── evaluator.py        # Module chạy thử nghiệm benchmark và so sánh
│   ├── flat_rag.py         # Cài đặt thuật toán Flat RAG
│   ├── graph_builder.py    # Xây dựng cấu trúc đồ thị tri thức
│   ├── graph_rag.py        # Cài đặt thuật toán truy vấn GraphRAG
│   └── visualizer.py       # Trực quan hóa và vẽ đồ thị thành tệp hình ảnh
```

## Quy trình triển khai

### Bước 1: Khởi tạo Môi trường ảo và Cài đặt Thư viện

```bash
# Tạo môi trường ảo mới
python -m venv venv

# Kích hoạt môi trường ảo (Windows)
venv\Scripts\activate

# Cài đặt toàn bộ các gói thư viện cần thiết
pip install -r requirements.txt
```

### Bước 2: Cài đặt Biến Môi trường

Tạo tệp cấu hình `.env` dựa trên tệp mẫu `.env.example` và thiết lập khóa API OpenAI của bạn:
```bash
cp .env.example .env
```
Mở tệp `.env` vừa tạo và điền thông tin: `OPENAI_API_KEY=your_openai_api_key_here`

### Bước 3: Thiết lập Tập dữ liệu

Người dùng có thể thực hiện theo một trong hai cách:
- **Cách 1**: Di chuyển tệp nén `dataset.zip` vào thư mục `data/`. Hệ thống sẽ tự động nhận diện và giải nén khi chạy chương trình.
- **Cách 2**: Giải nén thủ công và đặt toàn bộ các tệp `.txt` vào trong thư mục `data/dataset/`.

### Bước 4: Vận hành chương trình

```bash
python main.py
```
Giao diện bảng chọn (Menu) sẽ hiển thị với các tùy chọn sau:
1. **Build pipeline**: Chạy toàn bộ quy trình từ tải dữ liệu, bóc tách quan hệ triples, xây dựng đồ thị, trực quan hóa và lập chỉ mục Vector.
2. **Ask with Flat RAG**: Thử nghiệm truy vấn bằng mô hình Flat RAG.
3. **Ask with GraphRAG**: Thử nghiệm truy vấn bằng mô hình GraphRAG.
4. **Run evaluation**: Thực hiện đánh giá so sánh tự động trên bộ 20 câu hỏi và lưu kết quả.
5. **Exit**: Thoát chương trình.

## Kết quả cần bàn giao
1. Toàn bộ mã nguồn dự án.
2. Biểu đồ trực quan hóa đồ thị tri thức: `outputs/knowledge_graph.png`.
3. Bảng kết quả đánh giá thực nghiệm: `outputs/evaluation.csv` và `outputs/evaluation.md`.
4. **Báo cáo phân tích ngắn gọn**: Nội dung chi tiết tại `outputs/analysis.md` so sánh rõ ưu nhược điểm của hai giải pháp. Flat RAG chiếm ưu thế về thời gian và chi phí vận hành nhưng dễ gặp lỗi ảo giác ngữ cảnh. GraphRAG tối ưu về tính chính xác và khả năng kết nối tri thức phức tạp nhưng tốn kém tài nguyên API và thời gian khởi tạo.

