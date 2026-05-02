Dưới đây là bảng tổng hợp chi tiết **8 Mục tiêu phân tích cốt lõi** và các loại biểu đồ tương ứng để bạn xây dựng Dashboard trên **Streamlit** (sử dụng thư viện `Plotly`). Nội dung được hệ thống hóa dựa trên báo cáo đồ án của nhóm bạn[cite: 2, 3].

---

# 🚀 Kế hoạch Trực quan hóa Đồ án Tiki Electronics 2026

## MT1: Thị phần Doanh số — Ai bán nhiều nhất?
**Mục tiêu:** So sánh sự đối đầu giữa "Số lượng mẫu mã" và "Hiệu quả thực tế" của Global Brand vs. Local/OEM[cite: 2, 3].
*   **Donut Chart:** Tỷ lệ % tổng lượng bán (Sum of `quantity_sold`) theo `brand_type`[cite: 2].
*   **Pie Chart:** Tỷ lệ % số lượng mẫu mã (Count of `product_id`) theo `brand_type`[cite: 2].
*   **100% Stacked Bar Chart:** Phân rã thị phần doanh thu theo từng danh mục (`category_name`)[cite: 2].
*   **Combo Chart (Bar + Line):** So sánh Tổng lượng bán và Trung bình lượng bán trên mỗi sản phẩm (`Avg Qty Per Product`)[cite: 2].

## MT2: Phân khúc Thị trường — Ai thống lĩnh vùng giá nào?
**Mục tiêu:** Xác định "vùng xanh" và "vùng đỏ" cạnh tranh theo các dải giá[cite: 3].
*   **100% Stacked Bar Chart:** Tỷ lệ lượng bán của Global vs. Local trong 5 phân khúc giá (Dưới 100K -> Trên 5M)[cite: 3].
*   **Clustered Bar Chart:** Tổng lượng bán theo từng dải giá để tìm "điểm rơi" thị trường[cite: 3].
*   **Heatmap (Density):** Mật độ phân bổ sản phẩm theo Ngành hàng x Dải giá[cite: 3].

## MT3: Price Premium — Giá chênh lệch bao nhiêu?
**Mục tiêu:** Đo lường quyền lực định giá và "phí thương hiệu"[cite: 2, 3].
*   **Boxplot:** Phân bổ dải giá, độ biến động và các giá trị ngoại lai (outliers) của hai nhóm thương hiệu[cite: 2].
*   **Median Price Bar Chart:** So sánh trực diện giá trung vị theo từng danh mục (`category_name`)[cite: 2].
*   **Heatmap:** Làm nổi bật các "điểm nóng" giá trung vị giữa các nhóm thương hiệu[cite: 2].

## MT4: Chiến lược Giảm giá — Ai giảm mạnh hơn?
**Mục tiêu:** Phân tích cuộc đua khuyến mãi và mức độ "cắt máu" để giành thị phần[cite: 2, 3].
*   **Stacked Bar Chart:** Tỷ lệ sản phẩm theo nhãn giảm giá (`discount_flag`: Extreme, Normal, No Discount)[cite: 2].
*   **Boxplot:** Phân bổ biên độ % giảm giá (`discount_rate`) để tìm các cú "giảm giá hủy diệt"[cite: 2].
*   **Grouped Bar Chart:** Mức giảm giá trung bình chia theo từng danh mục sản phẩm[cite: 2].

## MT5: Tiki Trading vs. Third-Party — Kênh nào hiệu quả hơn?
**Mục tiêu:** Kiểm chứng sức mạnh của "official store" và hệ sinh thái Tiki[cite: 2, 3].
*   **Bar Charts:** So sánh trực tiếp Lượng bán trung bình, Số Review trung bình và Rating trung bình giữa 2 kênh[cite: 2].
*   **Violin Plot (Log Scale):** Phân tích sự phân tán doanh số để thấy xác suất một sản phẩm thành công trên mỗi kênh[cite: 2].
*   **Stacked Bar Chart:** Tỷ lệ sản phẩm được Tiki lựa chọn phân phối (`curation strategy`) theo loại thương hiệu[cite: 2].

## MT6: Tỷ lệ Chuyển đổi — Brand nào dễ bán hơn?
**Mục tiêu:** Tìm "tấm vé thông hành" giúp sản phẩm mới thoát khỏi tình trạng không đơn hàng[cite: 2, 3].
*   **100% Stacked Bar Chart:** Tỷ lệ "Đã bán" (has_sales) vs. "Chưa bán" (new_listing) của Global vs. Local[cite: 2].
*   **Matrix Heatmap:** Tỷ lệ chuyển đổi (%) khi kết hợp giữa Nhóm thương hiệu x Kênh phân phối[cite: 2].
*   **Horizontal Bar Chart:** Xếp hạng tỷ lệ chuyển đổi theo 12 danh mục sản phẩm[cite: 2].

## MT7: Độ tin cậy hệ thống Đánh giá — Bóc tách Rating nghi vấn
**Mục tiêu:** Nhận diện các thủ thuật "buff rating" và niềm tin ảo[cite: 2, 3].
*   **Heatmap-style Bar Chart:** Xếp hạng % Rating nghi vấn (Rating > 4.5, Review < 10) theo danh mục[cite: 2].
*   **Comparative Bar Chart:** So sánh điểm Rating trung bình giữa nhóm "Bình thường" vs. nhóm "Nghi vấn"[cite: 2].
*   **100% Stacked Bar Chart:** Tỷ trọng sản phẩm Nghi vấn giữa Global Brand và Local/OEM[cite: 2].

## MT8: Các yếu tố ảnh hưởng Doanh số — Tìm "điểm bùng phát"
**Mục tiêu:** Tìm mối tương quan kỹ thuật giữa các biến số[cite: 3].
*   **Scatter Plot:** Tương quan giữa Số lượng Review vs. Tổng lượng bán[cite: 3].
*   **Scatter Plot:** Tương quan giữa Điểm Rating trung bình vs. Lượng bán[cite: 3].
*   **Pearson Correlation Matrix (Heatmap):** Chỉ số tương quan giữa Giá, Rating, Review và Lượng bán[cite: 3].

---

### 💡 Lưu ý triển khai trên Streamlit cho nhóm Hoàng Anh:
*   **Interactive Slicers:** Sử dụng `st.sidebar.multiselect` để lọc theo `category_name` và `brand_type` cho toàn bộ các biểu đồ trên.
*   **AI Insight Section:** Sử dụng kết quả từ **MT3** và **MT8** làm đầu vào cho Gemini API để sinh ra các nhận xét chiến lược tự động.
*   **Logging:** Đừng quên hàm lưu vết các Prompt vào file CSV để nộp kèm báo cáo[cite: 2].