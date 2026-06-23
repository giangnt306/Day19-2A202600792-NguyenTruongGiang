# Báo cáo Phân tích Chi phí Thời gian và Tài nguyên (Token) trong Hệ thống GraphRAG & Flat RAG
Họ và Tên: Hoàng Văn Anh - MSSV: 2A202600762

**1. Phân tích về mặt Thời gian (Execution Time):**
*   **Flat RAG:** Rất tối ưu về tốc độ. Quá trình tạo vector embeddings và index cho toàn bộ tập dữ liệu (70 tài liệu) diễn ra gần như tức thì, chỉ mất vài giây nhờ sử dụng mô hình embedding cục bộ.
*   **GraphRAG:** Đòi hỏi lượng thời gian khởi tạo rất lớn (từ vài phút cho tới hàng chục phút). Nguyên nhân chính là do giai đoạn Trích xuất Thực thể và Quan hệ (Entity-Relation Extraction) bắt buộc phải gửi yêu cầu tuần tự hoặc song song đến LLM thông qua API cho từng phân đoạn văn bản (chunk), dẫn đến độ trễ mạng và giới hạn xử lý của mô hình.

**2. Phân tích về mặt Token tiêu hao (Token Usage):**
*   **Flat RAG:** Chi phí cực kỳ thấp ở giai đoạn lập chỉ mục (Indexing). Các mô hình biểu diễn từ như `all-MiniLM-L6-v2` chạy trực tiếp trên thiết bị (local) hoàn toàn miễn phí, không phát sinh chi phí token API.
*   **GraphRAG:** Tiêu tốn một lượng tài nguyên khổng lồ. Việc yêu cầu LLM phân tích ngữ nghĩa để rút trích các mối quan hệ (triples) từ 70 văn bản tạo ra hàng trăm nghìn token (cả prompt và output), dễ dàng chạm các hạn mức Rate Limit (RPM/TPM) của nhà cung cấp dịch vụ.

**3. Đánh giá và Kết luận:**
Tóm lại, GraphRAG đòi hỏi chi phí đầu tư ban đầu rất lớn cả về thời gian lập chỉ mục lẫn chi phí tài chính cho API so với Flat RAG. Tuy nhiên, sự đầu tư này hoàn toàn xứng đáng khi bước vào giai đoạn truy vấn. GraphRAG vượt trội hơn hẳn Flat RAG ở khả năng hạn chế tối đa hiện tượng "ảo giác" (hallucination). Khi gặp các câu hỏi mang tính suy luận bắc cầu hoặc yêu cầu tổng hợp thông tin phức tạp liên kết giữa nhiều thực thể, GraphRAG cung cấp câu trả lời chính xác, mạch lạc nhờ cấu trúc đồ thị tri thức chặt chẽ, thay vì chỉ tìm kiếm độ tương đồng vector đơn giản như Flat RAG.

