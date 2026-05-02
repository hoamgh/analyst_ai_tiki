📝 Hệ thống Dashboard Phân tích Tiki Electronics 2026
1. Kiến trúc Hệ thống (System Architecture)
Hệ thống được xây dựng theo mô hình End-to-End Data Pipeline.  

Tầng Dữ liệu: File tiki_clean_data.csv (Dữ liệu đã qua Pipeline 7 giai đoạn, >10,000 dòng).  

Tầng Xử lý (Logic): Python (Pandas) thực hiện các phép tính thống kê và lọc dữ liệu thời gian thực.

Tầng Trình diễn (UI): Streamlit cung cấp giao diện tương tác với người dùng qua Sidebar và Tabs. sử dụng cái mục tiêu trong (muc tieu md)

Tầng Thông minh (AI): Gemini API nhận kết quả thống kê để sinh ra nhận xét chiến lược.