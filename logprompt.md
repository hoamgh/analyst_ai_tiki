Yêu cầu bắt buộc
Mọi phản hồi từ AI Agent khi tương tác với người dùng trên Dashboard đều phải được ghi vết (log) để phục vụ báo cáo đồ án.  

2. Cấu trúc Nhật ký (prompt_logs.csv)
Ghi dữ liệu theo các cột sau (ngắn gọn, bỏ qua timestamp nếu hệ thống tự động đã có):

Objective: Mã mục tiêu (MT1 - MT8).  

User_Query: Câu hỏi thực tế từ người dùng.

System_Context: Dữ liệu thống kê tĩnh (Metadata) được gửi kèm.

AI_Response: Câu trả lời cuối cùng của Agent.

3. Nguyên tắc nội dung
Chỉ dựa trên Data: Phản hồi phải bám sát kết quả từ statsmodels hoặc describe() của bộ dữ liệu Tiki.  

Minh bạch: Ghi lại chính xác những gì AI đã "đọc" được từ dữ liệu văn bản để đối chiếu với biểu đồ.

Xác thực: Nhật ký này là minh chứng cho tiêu chí "Tích hợp AI" trong đồ án.

4. Checklist thực thi (Dành cho Agent)
Nhận User Query.

Truy xuất Static Context tương ứng với mục tiêu.

Sinh phản hồi.

LƯU VẾT vào file ngay lập tức trước khi hiển thị kết quả.