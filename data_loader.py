"""
data_loader.py — Tầng Dữ liệu
Load file CSV và thực hiện Feature Engineering cho toàn bộ Dashboard.
"""
import pandas as pd
import streamlit as st
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "tiki_electronics_2026.csv")

# ── Phân khúc giá (dùng cho MT2) ──────────────────────────────────────
PRICE_BINS  = [0, 100_000, 500_000, 2_000_000, 5_000_000, float("inf")]
PRICE_LABELS = ["Dưới 100K", "100K – 500K", "500K – 2M", "2M – 5M", "Trên 5M"]

# ── Nhãn giảm giá (dùng cho MT4) ──────────────────────────────────────
def _discount_flag(rate: float) -> str:
    if rate <= 0:
        return "No Discount"
    elif rate < 0.3:
        return "Normal"
    else:
        return "Extreme"


@st.cache_data(show_spinner="Đang tải dữ liệu Tiki…")
def load_data() -> pd.DataFrame:
    """Load và chuẩn bị dữ liệu, cache kết quả."""
    # Giải thích tự nhiên: Đoạn code này chỉ ĐỌC file CSV để tạo DataFrame trong bộ nhớ.
    # Không có thao tác ghi/ghi đè ngược lại file dữ liệu gốc.
    df = pd.read_csv(DATA_PATH)

    # ── Ép kiểu ──────────────────────────────────────────────────
    numeric_cols = ["price", "original_price", "discount_rate",
                    "rating_average", "review_count", "quantity_sold"]
    for col in numeric_cols:
        # Giải thích tự nhiên: Đoạn code này ép kiểu các cột số.
        # - pd.to_numeric(..., errors="coerce") sẽ biến giá trị lỗi thành NaN
        # - fillna(0) sẽ thay NaN bằng 0 để tránh lỗi tính toán ở các biểu đồ/thống kê
        # (mọi thay đổi chỉ áp dụng trên DataFrame trong RAM, không sửa file CSV gốc).
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["is_tiki_trading"] = df["is_tiki_trading"].astype(int)

    # ── Feature Engineering ──────────────────────────────────────
    # Doanh thu ước tính
    # Giải thích tự nhiên: Đoạn code này tạo cột doanh thu ước tính theo công thức
    # revenue = price * quantity_sold để phục vụ các biểu đồ doanh thu.
    df["revenue"] = df["price"] * df["quantity_sold"]

    # Phân khúc giá
    # Giải thích tự nhiên: Đoạn code này phân loại sản phẩm thành các "dải giá" bằng pd.cut(),
    # dựa trên PRICE_BINS/PRICE_LABELS để phục vụ phân tích phân khúc (MT2).
    df["price_segment"] = pd.cut(
        df["price"], bins=PRICE_BINS, labels=PRICE_LABELS, right=False
    )

    # Nhãn giảm giá
    df["discount_flag"] = df["discount_rate"].apply(_discount_flag)

    # Trạng thái bán
    df["has_sales"] = df["quantity_sold"].apply(
        lambda x: "Đã bán" if x > 0 else "Chưa bán"
    )

    # Kênh phân phối
    df["channel"] = df["is_tiki_trading"].apply(
        lambda x: "Tiki Trading" if x == 1 else "Third-Party"
    )

    # Rating nghi vấn (MT7)
    df["is_rating_suspect"] = (
        (df["rating_average"] > 4.5) & (df["review_count"] < 10)
    ).astype(int)

    df["suspect_label"] = df["is_rating_suspect"].apply(
        lambda x: "Nghi vấn" if x == 1 else "Bình thường"
    )

    # Avg Qty Per Product (tính theo brand_type)
    avg_qty = df.groupby("brand_type")["quantity_sold"].transform("mean")
    df["avg_qty_per_product"] = avg_qty

    return df
