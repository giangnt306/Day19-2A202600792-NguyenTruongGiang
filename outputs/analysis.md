# ĐÁNH GIÁ HIỆU NĂNG VÀ PHÂN TÍCH CHI PHÍ: GRAPHRAG VS FLAT RAG
**Sinh viên thực hiện:** Nguyễn Trường Giang  
**Mã số sinh viên (MSSV):** 2A202600792  

---

### 1. Khảo sát Hiệu năng Thời gian Xử lý (Execution Latency)
*   **Kiến trúc Standard (Flat) RAG:** 
    Giải pháp này mang lại tốc độ xử lý vượt trội. Bước số hóa ngữ liệu (text vectorization) và thiết lập chỉ mục FAISS trên 70 văn bản mẫu được hoàn thành chỉ trong thời gian tính bằng giây. Do tận dụng mô hình nhúng cục bộ (`all-MiniLM-L6-v2`), toàn bộ quy trình tính toán đều diễn ra trên phần cứng local, giúp triệt tiêu độ trễ mạng.
*   **Kiến trúc Đồ thị Tri thức (Knowledge Graph RAG):** 
    Ngược lại hoàn toàn, GraphRAG đòi hỏi thời gian tiền xử lý và xây dựng đồ thị tương đối lớn (có thể dao động từ 10 đến 30 phút tùy thuộc cấu hình song song). Sự chậm trễ này chủ yếu phát sinh từ việc gửi các yêu cầu bóc tách thực thể - quan hệ (triples extraction) tuần tự đến OpenAI API cho từng phần tài liệu, dẫn tới tổng thời gian chờ bị phụ thuộc trực tiếp vào băng thông và tốc độ xử lý phản hồi từ LLM Cloud.

### 2. Phân tích Tài nguyên và Token Tiêu hao (API Costs & Tokens)
*   **Kiến trúc Standard (Flat) RAG:** 
    Giai đoạn lập chỉ mục không làm phát sinh chi phí tài chính nào. Các mô hình SentenceTransformer hoạt động độc lập và hoàn toàn miễn phí trên máy chủ local. Chi phí duy nhất chỉ xuất hiện khi sinh câu trả lời cuối cùng từ ngữ cảnh đã lọc, giúp tối ưu hóa ngân sách vận hành hệ thống.
*   **Kiến trúc Đồ thị Tri thức (Knowledge Graph RAG):** 
    GraphRAG tiêu tốn một khoản chi phí API Token không hề nhỏ. Quá trình phân tích cú pháp ngữ nghĩa toàn bộ 70 văn bản để cấu trúc hóa thành Subject-Relation-Object đòi hỏi LLM phải đọc qua toàn bộ văn bản gốc và sinh ra lượng output JSON tương đối lớn. Điều này tạo ra hàng trăm nghìn prompt/completion tokens, đòi hỏi quản lý hạn mức API chặt chẽ để tránh lỗi quá tải (Rate Limits).

### 3. Nhận định Tổng quan và Kết luận Thực nghiệm
Dù GraphRAG yêu cầu tài nguyên ban đầu (cả về thời gian xây dựng lẫn chi phí tài chính API) cao hơn hẳn Flat RAG, cấu trúc này lại thể hiện ưu thế vượt trội khi phục vụ truy vấn thực tế. 

Standard RAG dựa trên tương đồng ngữ nghĩa vector phẳng dễ bị nhiễu và gặp lỗi "ảo giác" (hallucination) khi ngữ cảnh không khớp rõ ràng. Trong khi đó, GraphRAG với mô hình kết nối thực thể đa chiều (Multi-hop Knowledge Graph) đảm bảo câu trả lời được kiểm soát chặt chẽ theo các cạnh thực thể đã định nghĩa sẵn. Điều này giúp hệ thống phản hồi cực kỳ logic đối với các câu hỏi phức tạp, yêu cầu liên kết thông tin gián tiếp qua nhiều thực thể trung gian.
