1 Yêu cầu tích hợp AI
Tích hợp tính năng AI vào phân tích dữ liệu: có thể là ứng dụng độc lập hoặc
tích hợp vào dashboard hoặc tạo API để các ứng dụng khác sử dụng.
Khuyến khích tạo API để các ứng dụng khác sử dụng
1.1 Nguyên tắc cơ bản
• AI: Đóng vai trò
– trợ giúp đề xuất ý tưởng
– viết code dựa vào yêu cầu của người dùng
– trình bày kết quả phân tích với số liệu và hình ảnh, biểu đồ được
cung cấp bởi con người, không được tự ý thêm số liệu hay hình ảnh
khác.
• Con người: Đóng vai trò
– định hướng, đề xuất các yêu cầu phân tích, ra quyết định thực thi
code.
– nếu con người chưa biết, chưa có ý tưởng về cách phân tích như
thế nào thì có thể yêu cầu AI đưa ra các gợi ý, phương pháp để con
người lựa chọn.
• Thực thi code: phải trên môi trường local của người dùng. Không
được thực thi trên môi trường online.
2 Nguyên tắc “không thực thi ngầm”
AI không được phép tự ý thay đổi dữ liệu gốc hay âm thầm chạy các thuật
toán.
1
• Hiển thị code bắt buộc: Mỗi khi AI tạo code theo yêu cầu của con
người, nó bắt buộc phải hiển thị rõ ràng.
• Giải thích bằng ngôn ngữ tự nhiên: Ngay trên đoạn code đó, AI
phải đính kèm các dòng comment giải thích bằng ngôn ngữ tự nhiên:
“Đoạn code này sẽ xóa 15 dòng có giá trị NULL ở cột Doanh Thu, sử
dụng hàm dropna() của Pandas.”
2.1 Nguyên tắc phê duyệt
Thể hiện vai trò “Người quyết định”.
• Trạng thái chờ: Code do AI sinh ra ban đầu sẽ ở trạng thái “Chờ
duyệt”. Con người có thể thay đổi, bổ sung hoặc loại bỏ code này.
• Chỉnh sửa: Con người có quyền trực tiếp can thiệp, gõ sửa các tham
số trong đoạn code AI vừa viết (ví dụ: đổi giới hạn outlier từ 3 standard
deviations xuống 2).
• Chấp nhận & thực thi: Đoạn code chỉ được thực thi và trả về kết
quả/biểu đồ khi và chỉ khi con người chấp thuận.
2.2 Nguyên tắc lưu trữ
Hệ thống phải lưu trữ tất cả các yêu cầu, mã nguồn, kết quả phân tích và giải
thích để có thể truy xuất lại được.
3 Trong vấn đáp
Các nhóm sẽ được yêu cầu sử dụng module AI đã phát triển để trả lời các câu
hỏi phân tích dựa trên dữ liệu của nhóm và các câu hỏi phân tích đã chuẩn bị
sẵn, nhằm tránh lan man. Tuy nhiên, vẫn có thể được yêu cầu trả lời câu hỏi
ngoài lề để đánh giá mức độ linh hoạt của AI.
4 Gợi ý thiết kế
Phân chia cấu trúc API và Frontend
4.1 Phần Giao diện & Tương tác người dùng (Frontend)
Công nghệ phát triển giao diện Frontend là tùy chọn (có thể dùng Streamlit,
Gradio, React, hoặc các công cụ Dashboard có khả năng tương tác, …). Các
2
nhóm chỉ cần đảm bảo các chức năng cơ bản. Khuyến khích các nhóm tạo ra
những giao diện đẹp, trực quan, dễ sử dụng cho người dùng.
• Chức năng nhận yêu cầu:
– Ví dụ: Một ô chat hoặc form nhập liệu để người dùng gửi yêu cầu
phân tích/viết code cho AI.
• Chức năng xem & chỉnh sửa mã nguồn
• Chức năng phê duyệt
• Chức năng hiển thị kết quả
4.2 Phần API
• API AI (bắt buộc):
– Tiếp nhận yêu cầu từ Front-end.
– Gửi kèm ngữ cảnh (ví dụ: cấu trúc dữ liệu hiện có) cho mô hình
AI (Gemini/OpenAI) (được sử dụng local model).
– Yêu cầu AI trả về cả code và giải thích tương ứng; hoặc kết quả
trình bày.
• API Thực thi (bắt buộc):
– Tiếp nhận đoạn mã đã được con người “chỉnh sửa” và “phê duyệt”
từ frontend.
– Thực hiện chạy code trực tiếp trên dữ liệu tại máy.
– Thu thập kết quả (ảnh biểu đồ, bảng dữ liệu, logs) để trả về cho
frontend hiển thị.
• API Logs (bắt buộc):
– Lưu trữ tất cả các yêu cầu, mã nguồn, kết quả phân tích và giải
thích.

---

# Phần bổ sung: Đối chiếu yêu cầu ↔ hệ thống hiện tại (repo này)

Mục tiêu của phần này là giúp nhóm **giải trình rõ ràng** khi vấn đáp: AI đang làm gì, không làm gì, và các cơ chế kiểm soát đã triển khai ở đâu.

## 1) AI đang làm gì trong đồ án này?
- **Lựa chọn triển khai của nhóm (Case A):** Tích hợp AI trực tiếp vào Dashboard Streamlit (ứng dụng end-user), **không bắt buộc** phải mở REST API cho ứng dụng khác.
- **Ghi chú rubric:** Tách REST API (AI/Execute/Logs) là hướng **khuyến khích** để tái sử dụng cho hệ thống khác; nhóm có thể mở rộng sau nếu giảng viên yêu cầu.
- AI (Gemini) **chỉ sinh nhận xét/insight bằng văn bản** dựa trên “System Context” (chuỗi thống kê) được code Python tạo ra từ dữ liệu đang lọc.
- AI **không tự ý tạo số liệu mới**, không tự ý tạo biểu đồ mới, và **không gửi hình ảnh** (chỉ gửi text).

## 2) Con người quyết định ở đâu?
- Người dùng chọn **mục tiêu MT1–MT8** + bộ lọc sidebar (danh mục, loại thương hiệu).
- Người dùng nhập câu hỏi và bấm nút “Gửi câu hỏi”.
- Hệ thống chỉ thực hiện (i) trích xuất thống kê từ dataframe hiện tại, (ii) gọi Gemini để viết nhận xét, (iii) log lại toàn bộ phiên.

## 3) “Không thực thi ngầm” được hiểu và áp dụng thế nào?
- Repo này **không có tính năng AI sinh code để chạy** (AI không trả về Python code để thực thi).
- Các phép tính thống kê/OLS là **code cố định do nhóm viết** (Pandas/Statsmodels), chỉ chạy khi người dùng tương tác.
- Dữ liệu gốc (CSV) chỉ được **đọc** để tạo dataframe; không có thao tác ghi/ghi đè lên file dữ liệu gốc.

### Làm rõ: “AI sinh code” trong rubric là gì?
- Trong rubric, “AI sinh code” có thể được hiểu theo 2 ngữ cảnh:
	1) **AI runtime của sản phẩm** (Gemini/OpenAI) sinh ra code để chạy.
	2) **AI hỗ trợ lập trình** (ví dụ Copilot/ChatGPT) hỗ trợ nhóm viết source code của project.
- Repo hiện tại đang ở **ngữ cảnh (2)**: AI runtime (Gemini) **chỉ sinh nhận xét/insight bằng văn bản**, không sinh code để chạy.
- Để đáp ứng yêu cầu “giải thích bằng ngôn ngữ tự nhiên ngay trên đoạn code”, nhóm đã (và nên) đặt comment/docstring tiếng Việt ngay cạnh các bước xử lý dữ liệu quan trọng (ví dụ ép kiểu, fillna, dropna, tạo biến, hồi quy), giúp giảng viên đọc source là thấy rõ “đoạn code làm gì”.

## 4) Lưu trữ (Logging) đã triển khai ra sao?
- Mọi tương tác AI đều được ghi vào `prompt_logs.csv` theo các trường:
	- Timestamp | Objective | User_Query | System_Context | AI_Response
- Mục đích: chứng minh tính minh bạch và khả năng truy xuất lại “AI đã đọc gì → trả lời gì”.

## 5) Vị trí các thành phần trong code
- UI Streamlit: `app.py`
- Component “Hỏi AI”: `ai_section.py`
- Trích xuất thống kê làm System Context: `stats_engine.py` (hàm `build_context_for_mt`)
- Gọi Gemini API và ép luật trả lời theo số liệu: `gemini_helper.py`
- Ghi log: `log_helper.py`
- Nạp dữ liệu + feature engineering: `data_loader.py`

---

# Checklist nộp bài / vấn đáp (khuyến nghị)

## A) Những câu thầy hay hỏi
1. AI có “bịa” số không? → Trả lời: Không. Vì prompt bắt buộc bám System Context (bảng thống kê/OLS), thiếu dữ liệu thì từ chối.
2. AI có chạy code ngầm không? → Không có AI-generated code execution; mọi phân tích là hàm thống kê cố định.
3. Log nằm ở đâu? → `prompt_logs.csv`.
4. Có tách API không? → Hiện tại tích hợp trong Streamlit; nếu rubric yêu cầu REST API, cần bổ sung FastAPI.

## B) Các điểm còn thiếu/rủi ro nên sửa trong tài liệu (và/hoặc hệ thống)
1. **Tách API**: Tài liệu gợi ý 3 API (AI/Execute/Logs). Repo hiện tại là “monolith Streamlit” (chưa có endpoint cho app khác gọi).
2. **Lưu trữ đầy đủ**: Nếu System Context quá dài, việc cắt ngắn khi ghi CSV có thể làm giảm khả năng chứng minh. Nếu thầy chấm gắt, nên lưu đầy đủ System Context.
3. **Giải thích cơ chế phê duyệt code**: Vì repo không cho AI sinh code để thực thi, cần nói rõ “không áp dụng workflow approve/run code”, tránh bị hỏi vặn.
4. **Tránh diễn đạt gây hiểu nhầm**: Nếu trong nơi khác có câu “local model”, cần chỉnh lại thành “Gemini API” (nếu nhóm dùng cloud) hoặc mô tả đúng giải pháp.
