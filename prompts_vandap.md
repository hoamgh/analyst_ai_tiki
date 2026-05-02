# Danh sách prompt để giải trình / vấn đáp
_Tạo tự động lúc: 2026-05-02 15:11:47_

Mục đích: gom lại những câu bạn đã hỏi Copilot trong quá trình làm đồ án, kèm một bộ prompt demo/hỏi-đáp hợp lý để trình bày với giảng viên.

## A) Prompt bạn đã hỏi Copilot (trích từ transcript)
**1.**

```text
Các rủi ro còn lại (chưa sửa vì liên quan phạm vi/thiết kế)

Kiến trúc hiện là Streamlit monolith, chưa tách REST API riêng cho AI/Execute/Logs (nếu thầy bắt buộc “API” đúng nghĩa thì có thể bị hỏi).
Rubric có phần “phê duyệt & thực thi code AI sinh ra”, nhưng repo hiện không có AI sinh code để chạy → cần giải trình rõ như mình đã ghi trong Aipriciple.md.
Muốn mình tách thêm FastAPI 3 endpoint (AI/Logs/Execute) để “đúng rubric API” luôn không?

phần này bản giaari thích đc k tôi chưa hiểu
```
**2.**

```text
trường hợp A là ứng dụng độc lập hoặc tích hợp vào dashboard hả
```
**3.**

```text
Vậy làm trường hợp A k cần tạo API cho ứng dụng khác đâu
```
**4.**

```text
bạn nghĩ tôi nên dùng API Ai nào (free)
```
**5.**

```text
bạn thử chạy app cho tôi xem đi
```
**6.**

```text
chạy bằng anaconda base có sẵn
```
**7.**

```text
Lỗi Gemini API: 404 models/gemini-1.5-flash is not found for API version v1beta, or is not supported for generateContent. Call ListModels to see the list of available models and their supported methods.
```
**8.**

```text
Dữ liệu được cung cấp không chứa thông tin về "danh mục" sản phẩm. Doanh thu được thống kê dựa trên "brand_type" (Thương hiệu toàn cầu và Thương hiệu địa phương/OEM chung), không phải theo danh mục cụ thể.

Vì vậy, không thể xác định danh mục nào có doanh thu cao nhất dựa trên dữ liệu hiện có.

nó hiện như này là sao
```
**9.**

```text
[BẢN TIN PHÂN TÍCH DỮ LIỆU TIKI — MT1]
Tổng sản phẩm: 10793
--- Thị phần Doanh số ---
| brand_type        |   count |    mean |   median |     std |    sum |
|:------------------|--------:|--------:|---------:|--------:|-------:|
| Global_Brand      |    4375 | 62.0633 |        1 | 699.252 | 271527 |
| Local/OEM Generic |    6418 | 19.0941 |        1 | 127.485 | 122546 |
Doanh thu:
| brand_type        |   count |        mean |   median |         std |          sum |
|:------------------|--------:|------------:|---------:|------------:|-------------:|
| Global_Brand      |    4375 | 2.37913e+07 |   138000 | 2.88855e+08 | 104087049068 |
| Local/OEM Generic |    6418 | 4.45637e+06 |    13400 | 3.23055e+07 |  28600987673 |

chỉ gửi cho AI từng này là chưa đủ bạn nghĩ là nên gửi những gì cho đủ
```
**10.**

```text
lệnh chạy streamlit là gì
```
**11.**

```text
tôi nghĩ là nên phân tích hết sau đó từng mục tiêu gửi những thứ cần thiết cho mục tiêu đó để làm ngữ cảnh cho AI
```
**12.**

```text
Chào bạn,

Dữ liệu hiện tại không đủ để xác định "giá của ngành hàng nào cao thứ 2 (Local/OEM Generic)". Lý do:

Bảng "Mật độ sản phẩm: Danh mục × Phân khúc giá" cung cấp số lượng sản phẩm theo danh mục và phân khúc giá, nhưng không phân biệt loại thương hiệu (Global_Brand hay Local/OEM Generic).
Bảng "Lượng bán theo Phân khúc giá × Loại thương hiệu" phân biệt lượng bán theo loại thương hiệu và phân khúc giá, nhưng không cung cấp thông tin theo danh mục sản phẩm.
Do đó, không thể kết hợp dữ liệu để tìm ra ngành hàng có giá cao nhất cho riêng thương hiệu Local/OEM Generic.

tôi hỏi như này nó trả lời k đúng bạn mình nghĩ là p phân tích đầy đủ cả data để người dùng hỏi còn biết đi
```
**13.**

```text
đừng dùng kiểu đó mình p gửi hết 1 lượt cho AI đi chứ k p phân tích từ câu hỏi
```
**14.**

```text
đổi theme đi khó nhìn quá làm sao cho dễ nhìn đi bộ lọc bây giờ khá khó sử dụng và các trang nó nằm cũng chưa hợp lý
```
**15.**

```text
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
phần của tôi đã có những phần này chưa
```
**16.**

```text
Giải thích bằng ngôn ngữ tự nhiên: Ngay trên đoạn code đó, AI
phải đính kèm các dòng comment giải thích bằng ngôn ngữ tự nhiên:
“Đoạn code này sẽ xóa 15 dòng có giá trị NULL ở cột Doanh Thu, sử
dụng hàm dropna() của Pandas.
đoạn này có chưa
```
**17.**

```text
AI sinh code ở đây là code của từng file trong project là bạn á k p AI là api tôi gọi
```
**18.**

```text
clear những thứ k thừa đi đừng đụng vào crawl
```
**19.**

```text
phần ols làm bằng step -wise đi
```
**20.**

```text
sửa lại phần bộ lọc cho đẹp đi
```
**21.**

```text
bạn tạo ra 1 file những câu prompt tôi đã hỏi bạn và thêm 1 vài câu đi (hợp lí) để giải trình với thầy
```

## B) Prompt bạn đã hỏi AI trong app (trích từ prompt_logs.csv)
- Ph
- danh mục nào doanh thu cao nhất
- danh mục nào có doanh thu cao nhất
- em yêu anh k
- giá của ngành hàng nào cao thứ 2 ( local_brand)
- mức giá chênh lệch giữa local và global có nhiều k
- xem coi ai bán nhiều hơn và ai doanh thu nhiều hơn

## C) Prompt gợi ý thêm (để demo & giải trình)

Lưu ý: Các prompt ở mục C là gợi ý/kịch bản để bạn dùng khi vấn đáp (không nhất thiết là các câu bạn đã hỏi trước đó).

### Giải trình (thầy hay hỏi)
- AI có bịa số liệu không? Nếu không, cơ chế nào đảm bảo?
- AI có tự ý thay đổi dữ liệu gốc không? Nhóm chứng minh bằng cách nào?
- Khi dữ liệu không đủ để kết luận, hệ thống xử lý thế nào?
- Log lưu ở đâu, lưu những gì, và truy xuất lại ra sao?
- Vì sao nhóm chọn tích hợp AI trong Streamlit thay vì tách REST API? Nếu cần thì tách được không?

### Prompt demo nhanh theo MT (hợp lý)
- (MT1) Top 3 danh mục đóng góp doanh thu cao nhất là gì? Global vs Local khác nhau ra sao (kèm số liệu %)?
- (MT2) Phân khúc giá nào là 'điểm rơi' về lượng bán? Trong phân khúc đó Global hay Local chiếm ưu thế?
- (MT3) Danh mục nào có chênh lệch giá trung vị Global vs Local lớn nhất?
- (MT4) Brand type nào có xu hướng giảm giá 'Extreme' nhiều hơn? Tỷ lệ % cụ thể?
- (MT5) Tiki Trading hay Third-Party có hiệu quả tốt hơn theo (qty/review/rating)?
- (MT6) Danh mục nào có conversion_rate cao nhất và thấp nhất? Gợi ý hành động?
- (MT7) Danh mục nào có % rating nghi vấn cao nhất? Có đáng lo không?
- (MT8) Step-wise OLS chọn biến nào ảnh hưởng tới quantity_sold? Dấu (+/-) và ý nghĩa?

### Prompt kiểm thử tính 'không lan man'
- Chỉ trả lời dựa trên số liệu trong System Context. Nếu thiếu số liệu, hãy nói 'không đủ dữ liệu'.
- Hãy trích đúng các con số (%, median, sum) từ bảng context để chứng minh.

### Prompt để chứng minh bạn tự chạy/tự làm (không nhờ chạy hết)
- Mình sẽ tự chạy app ở máy mình; bạn chỉ đưa lệnh chạy và cách set biến môi trường cần thiết.
- Mình đã tự chạy và gặp lỗi X; bạn giúp đọc stacktrace và chỉ đúng vị trí cần sửa (mình tự sửa code).
- Đây là diff mình vừa sửa; bạn review nhanh xem có phá gì không và có chỗ nào nên chỉnh cho sạch hơn.
- Bạn giúp mình viết checklist manual test cho từng MT (mình tự test, bạn chỉ cần gợi ý case).
- Mình muốn giữ nguyên `crawler/`; bạn chỉ ra chỗ nào có thể clean mà không đụng vào crawl.
- Mình muốn tự triển khai step-wise OLS; bạn chỉ gợi ý thuật toán/tiêu chí (AIC/BIC) và mình tự code theo.
- Bạn giúp mình viết câu giải trình: mình dùng AI để gợi ý/soát lỗi, còn chạy app + tạo biểu đồ + phân tích là do mình thực hiện.
