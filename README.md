# Dự án Đối chiếu và Thực nghiệm: Knowledge Graph RAG vs Flat Vector RAG
**Sinh viên thực hiện:** Nguyễn Trường Giang  
**MSSV:** 2A202600792  

---

Dự án này tập trung triển khai và so sánh hiệu quả tìm kiếm, truy xuất thông tin giữa hai kiến trúc phổ biến trong các hệ thống RAG (Retrieval-Augmented Generation):
1.  **Flat Vector RAG (Standard RAG):** Sử dụng thư viện `faiss-cpu` để lập chỉ mục phẳng vector, kết hợp mô hình cục bộ `sentence-transformers` nhằm tính toán độ tương đồng cosine ngữ nghĩa giữa truy vấn và ngữ liệu thô.
2.  **Knowledge Graph RAG (GraphRAG):** Rút trích các thực thể và mối quan hệ (triples) thông qua OpenAI API, xây dựng đồ thị tri thức đa chiều bằng thư viện `networkx`, sau đó truy xuất mở rộng 2-hop lân cận để cung cấp ngữ cảnh trả lời có cấu trúc và logic chặt chẽ.

## Sơ đồ Cấu trúc Dự án

```text
.
├── .env                    # Lưu khóa cấu hình API (OPENAI_API_KEY)
├── .env.example            # Bản tệp mẫu cho các cấu hình môi trường
├── main.py                 # Điểm khởi chạy chính và giao diện dòng lệnh
├── README.md               # Hướng dẫn chi tiết dự án
├── requirements.txt        # Danh sách thư viện và dependencies cần thiết
├── data/
│   └── dataset/            # Chứa các tài liệu ngữ liệu định dạng .txt
├── outputs/                # Thư mục xuất các kết quả phân tích thực nghiệm
│   ├── analysis.md         # Báo cáo đánh giá chi phí tài nguyên và thời gian
│   ├── evaluation.csv      # Bảng ghi nhận kết quả đánh giá 20 câu hỏi (CSV)
│   ├── evaluation.md       # So sánh đối chiếu hiệu năng chi tiết giữa 2 RAG
│   ├── graph.json          # Đồ thị tri thức được lưu trữ dưới dạng Node-Link JSON
│   ├── knowledge_graph.png # Biểu đồ trực quan hóa đồ thị (Top 50 nodes lớn nhất)
│   └── triples.json        # Bản lưu cache các quan hệ bóc tách từ tài liệu
└── src/
    ├── loader.py           # Quản lý nạp tài liệu và giải nén dữ liệu mẫu
    ├── extractor.py        # Module bóc tách thực thể - quan hệ sử dụng LLM
    ├── builder.py          # Thiết lập cấu trúc đồ thị từ các bộ ba triples
    ├── plot.py             # Vẽ đồ thị tri thức ra định dạng hình ảnh Matplotlib
    ├── rag_flat.py         # Quy trình Flat Vector RAG
    ├── rag_graph.py        # Quy trình Graph-based RAG
    └── evaluation.py       # Kịch bản chạy đánh giá benchmark tự động
```

## Các Bước Triển Khai Thực Nghiệm

### Bước 1: Chuẩn bị Môi trường và Dependencies

Khởi tạo môi trường ảo Python và tiến hành cài đặt các thư viện cần thiết:
```bash
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường ảo
source venv/bin/activate  # Trên Linux/macOS
# Hoặc: venv\Scripts\activate  # Trên Windows

# Cài đặt toàn bộ dependencies
pip install -r requirements.txt
```

### Bước 2: Thiết lập Cấu hình API

Sao chép tệp cấu hình mẫu `.env.example` thành tệp hoạt động thực tế `.env`:
```bash
cp .env.example .env
```
Mở tệp `.env` vừa tạo và cập nhật khóa OpenAI của bạn:
`OPENAI_API_KEY=your_openai_api_key_here`

### Bước 3: Đặt Dữ liệu Ngữ liệu

Có hai cách để chuẩn bị dữ liệu đầu vào:
*   **Cách 1:** Di chuyển file nén dữ liệu `dataset.zip` vào thư mục `data/`. Hệ thống sẽ tự động nhận diện và giải nén khi khởi động chương trình.
*   **Cách 2:** Đặt trực tiếp các file văn bản (.txt) của bạn vào thư mục `data/dataset/`.

### Bước 4: Vận hành và Chạy Thử nghiệm

Khởi chạy menu dòng lệnh bằng lệnh sau:
```bash
python main.py
```
Giao diện điều khiển bao gồm 5 tùy chọn tương tác:
1.  **Build and Run Pipeline:** Chạy toàn bộ quy trình tiền xử lý, rút trích triples, thiết lập KG, lưu đồ thị dạng ảnh và lập chỉ mục Vector RAG.
2.  **Retrieve and Answer using Flat Vector RAG:** Nhập câu hỏi và kiểm tra phản hồi từ Standard RAG.
3.  **Retrieve and Answer using Knowledge Graph RAG:** Nhập câu hỏi và kiểm tra phản hồi từ GraphRAG.
4.  **Perform Benchmark Evaluation:** Chạy thử nghiệm trên bộ 20 câu hỏi so sánh và xuất báo cáo tự động.
5.  **Exit Program:** Thoát chương trình.

## Danh sách Tài liệu Bàn giao (Deliverables)
1.  Toàn bộ mã nguồn hoàn chỉnh đã được tái cấu trúc (`main.py`, thư mục `src/`, `requirements.txt`).
2.  Sơ đồ trực quan hóa đồ thị tri thức: `outputs/knowledge_graph.png`.
3.  Bảng thống kê kết quả benchmark 20 câu hỏi: `outputs/evaluation.csv` và `outputs/evaluation.md`.
4.  Báo cáo phân tích chi phí thời gian và token: `outputs/analysis.md`.
