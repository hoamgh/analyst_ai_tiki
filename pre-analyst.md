

# 📑 PROTOCOL: PRE-ANALYSIS & DATA-DRIVEN RESPONSE

## 1. Nguyên tắc cốt lõi (Core Principle)
Để đảm bảo tính chính xác tuyệt đối cho đồ án Trực quan hóa, AI Agent chỉ được phép phản hồi sau khi dữ liệu đã được xử lý qua tầng phân tích kỹ thuật (Technical Analysis Layer)[cite: 2].

## 2. Quy trình 3 bước (The 3-Step Flow)

### Bước 1: Trích xuất Dữ liệu (Extraction)
Trước khi gửi câu hỏi cho AI, hệ thống (code Python/Streamlit) thực hiện:
*   **Thống kê mô tả:** Chạy `df.describe()` trên tập dữ liệu đang hiển thị để lấy giá trung bình, lượng bán, rating[cite: 2, 3].
*   **Phân tích kỹ thuật:** Lấy kết quả từ mô hình hồi quy `statsmodels` (hệ số tương quan, P-value).
*   **Lọc dữ liệu nghi vấn:** Xác định số lượng sản phẩm bị gắn cờ `is_rating_suspect` hoặc `fake_discount`[cite: 2].

### Bước 2: Đóng gói Ngữ cảnh (Context Packaging)
Toàn bộ kết quả ở Bước 1 được chuyển đổi thành chuỗi văn bản (String) và lồng vào **System Prompt**. 
*   *Lưu ý:* Tuyệt đối không gửi hình ảnh biểu đồ, chỉ gửi các con số và văn bản.

### Bước 3: Phản hồi dựa trên Chứng cứ (Evidence-based Response)
AI Agent nhận gói dữ liệu và thực hiện:
*   **Đối chiếu:** So sánh câu hỏi của người dùng với các con số trong ngữ cảnh được cung cấp.
*   **Nhận xét:** Chỉ ra các xu hướng (Trends), điểm bất thường (Outliers) hoặc mối quan hệ giữa các biến dựa trên số liệu thực.
*   **Từ chối:** Nếu dữ liệu trích xuất không chứa thông tin liên quan đến câu hỏi, Agent phải từ chối trả lời để tránh "chém gió" (Hallucination).

## 3. Cấu trúc Prompt mẫu (Template)
```text
[BẢN TIN PHÂN TÍCH DỮ LIỆU TIKI]
- Thống kê: {df_metadata}
- Kết quả tương quan: {correlation_results}
- Cảnh báo Seeding: {suspect_rating_count}

[CÂU HỎI NGƯỜI DÙNG]
{user_query}

[YÊU CẦU]
Hãy phân tích và trả lời. Bắt buộc sử dụng số liệu ở trên để minh chứng.
```

## 4. Kiểm soát chất lượng (Logging)
Mọi quy trình "Phân tích -> Gửi -> Trả lời" này phải được ghi lại vào nhật ký `prompt_logs.csv` để làm bằng chứng về tính minh bạch của hệ thống AI trong đồ án[cite: 2].

---

Bạn hãy lưu tệp này với tên `PreAnalysis_Protocol.md`. Việc này giúp nhóm bạn (Hoàng Anh, Huy Hoàng, Chí Thạnh, Đức Thuận) giải trình rất thuyết phục trước các thầy về cách các bạn kiểm soát AI để nó không trả lời sai lệch số liệu thực tế của Tiki[cite: 2].