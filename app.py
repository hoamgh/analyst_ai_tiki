"""
🚀 Dashboard Phân tích Tiki Electronics 2026
Kiến trúc 4 tầng: Dữ liệu → Xử lý (Pandas) → Trình diễn (Streamlit) → AI (Gemini)
"""
import streamlit as st
import pandas as pd

# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Tiki Electronics 2026 — Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Base ── */
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background: #F7F8FA;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #FFFFFF;
    border-right: 1px solid rgba(17,24,39,0.12);
}

/* Sidebar headings */
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #111827 !important;
}

/* Main text */
.stMarkdown, .stCaption, .stText, p, label { color: #111827; }

/* ── Glass cards ── */
div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid rgba(17,24,39,0.10);
    border-radius: 12px;
    padding: 16px 20px;
}
div[data-testid="stMetric"] label { color: #374151 !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] {
    color: #111827 !important; font-weight: 700;
}

/* ── Expander ── */
details {
    background: #FFFFFF !important;
    border: 1px solid rgba(17,24,39,0.10) !important;
    border-radius: 10px !important;
}

/* ── AI Chat area ── */
.ai-response {
    background: rgba(21, 101, 192, 0.06);
    border-left: 4px solid #1565C0;
    border-radius: 8px;
    padding: 16px 20px;
    margin: 8px 0;
    color: #111827;
    line-height: 1.7;
}

/* ── Divider ── */
hr { border-color: rgba(17,24,39,0.10) !important; }
</style>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────
from data_loader import load_data

df_raw = load_data()

# ── Sidebar: Filters ────────────────────────────────────────────────
st.sidebar.markdown("# 🛒 Tiki Electronics 2026")
st.sidebar.caption("Dashboard Trực quan hóa + AI Insight")

with st.sidebar.expander("🔎 Bộ lọc", expanded=True):
    # Danh mục
    categories = sorted(df_raw["category_name"].dropna().unique().tolist())
    if "selected_cats" not in st.session_state:
        st.session_state["selected_cats"] = categories

    st.markdown("**Danh mục**")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Chọn tất cả", use_container_width=True, key="cats_all_btn"):
            st.session_state["selected_cats"] = categories
            st.rerun()
    with c2:
        if st.button("Bỏ chọn", use_container_width=True, key="cats_none_btn"):
            st.session_state["selected_cats"] = []
            st.rerun()

    selected_cats = st.multiselect(
        "",
        categories,
        key="selected_cats",
        placeholder="Gõ để tìm danh mục…",
        help="Bạn có thể gõ để tìm nhanh",
        label_visibility="collapsed",
    )
    st.caption(f"Đang chọn: {len(selected_cats)}/{len(categories)}")

    # Loại thương hiệu
    brand_types = sorted(df_raw["brand_type"].dropna().unique().tolist())
    if "selected_brands" not in st.session_state:
        st.session_state["selected_brands"] = brand_types

    st.markdown("**Loại thương hiệu**")
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Chọn tất cả", use_container_width=True, key="brands_all_btn"):
            st.session_state["selected_brands"] = brand_types
            st.rerun()
    with b2:
        if st.button("Bỏ chọn", use_container_width=True, key="brands_none_btn"):
            st.session_state["selected_brands"] = []
            st.rerun()

    selected_brands = st.multiselect(
        "",
        brand_types,
        key="selected_brands",
        placeholder="Chọn loại thương hiệu…",
        label_visibility="collapsed",
    )
    st.caption(f"Đang chọn: {len(selected_brands)}/{len(brand_types)}")

# Apply filters
df = df_raw[
    (df_raw["category_name"].isin(selected_cats)) &
    (df_raw["brand_type"].isin(selected_brands))
].copy()

# Giải thích tự nhiên: Đoạn code này tạo một bản copy() DataFrame sau lọc để đảm bảo
# các thao tác phía sau (tính toán thống kê/biểu đồ) không vô tình tác động ngược lên df_raw.

st.sidebar.markdown("---")
st.sidebar.metric("Sản phẩm hiển thị", f"{len(df):,}")
st.sidebar.caption(f"Tổng dataset: {len(df_raw):,} sản phẩm")

# ── Navigation ──────────────────────────────────────────────────────
MT_OPTIONS = [
    "MT1 — Thị phần Doanh số",
    "MT2 — Phân khúc Thị trường",
    "MT3 — Price Premium",
    "MT4 — Chiến lược Giảm giá",
    "MT5 — Tiki Trading vs Third-Party",
    "MT6 — Tỷ lệ Chuyển đổi",
    "MT7 — Độ tin cậy Rating",
    "MT8 — Yếu tố ảnh hưởng Doanh số",
]

# Gọn hơn radio (đỡ scroll), dễ dùng hơn
with st.sidebar.expander("🎯 Mục tiêu phân tích", expanded=True):
    if "selected_mt" not in st.session_state:
        st.session_state["selected_mt"] = MT_OPTIONS[0]
    selected_mt = st.selectbox(
        "Chọn mục tiêu",
        MT_OPTIONS,
        index=MT_OPTIONS.index(st.session_state["selected_mt"]),
        key="selected_mt",
    )

mt_code = selected_mt.split(" — ")[0]  # "MT1", "MT2", ...

# ── Import chart modules ─────────────────────────────────────────────
from charts import mt1, mt2, mt3, mt4, mt5, mt6, mt7, mt8

MT_MODULES = {
    "MT1": mt1, "MT2": mt2, "MT3": mt3, "MT4": mt4,
    "MT5": mt5, "MT6": mt6, "MT7": mt7, "MT8": mt8,
}

# ── Render selected MT ──────────────────────────────────────────────
module = MT_MODULES[mt_code]
module.render(df)

# ── Footer ──────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#616161; font-size:12px;'>"
    "📊 Đồ án Trực quan hóa Dữ liệu Tiki 2026 — "
    "Nhóm: Hoàng Anh · Huy Hoàng · Chí Thạnh · Đức Thuận<br>"
    "Pipeline: Python Crawler → S3 → Spark → SQL Server → Streamlit + Gemini AI"
    "</div>",
    unsafe_allow_html=True,
)
