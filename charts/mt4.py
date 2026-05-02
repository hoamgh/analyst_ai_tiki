"""
MT4: Chiến lược Giảm giá — Ai giảm mạnh hơn?
Biểu đồ: Stacked Bar (discount_flag), Boxplot discount_rate, Grouped Bar trung bình giảm giá
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from charts.theme import (
    BRAND_COLORS, DISCOUNT_COLORS, apply_theme, format_number
)

FLAG_ORDER = ["No Discount", "Normal", "Extreme"]


def stacked_bar_discount_flag(df: pd.DataFrame) -> go.Figure:
    """Stacked Bar: Tỷ lệ sản phẩm theo discount_flag per brand_type."""
    data = df.groupby(["brand_type", "discount_flag"]).size().reset_index(name="count")
    pivot = data.pivot_table(index="brand_type", columns="discount_flag",
                             values="count", fill_value=0)
    pivot = pivot.reindex(columns=FLAG_ORDER)
    total = pivot.sum(axis=1)
    pct = pivot.div(total, axis=0) * 100

    fig = go.Figure()
    for flag in FLAG_ORDER:
        if flag in pct.columns:
            fig.add_trace(go.Bar(
                x=pct.index,
                y=pct[flag],
                name=flag,
                marker_color=DISCOUNT_COLORS.get(flag, "#999"),
                text=[f"{v:.1f}%" for v in pct[flag]],
                textposition="inside",
                textfont=dict(size=13, color="#FFF"),
                hovertemplate=f"<b>{flag}</b><br>%{{x}}<br>Tỷ lệ: %{{y:.1f}}%<extra></extra>",
            ))
    fig.update_layout(
        barmode="stack",
        xaxis_title="Loại thương hiệu",
        yaxis_title="Tỷ lệ (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return apply_theme(fig, "📊 Tỷ lệ SP theo mức Giảm giá")


def boxplot_discount_rate(df: pd.DataFrame) -> go.Figure:
    """Boxplot: Phân bổ biên độ % discount_rate."""
    fig = go.Figure()
    for bt, color in BRAND_COLORS.items():
        sub = df[df["brand_type"] == bt]["discount_rate"]
        fig.add_trace(go.Box(
            y=sub * 100,  # chuyển sang %
            name=bt,
            marker_color=color,
            line_color=color,
            boxmean="sd",
        ))
    fig.update_layout(yaxis_title="Tỷ lệ giảm giá (%)", showlegend=False)
    return apply_theme(fig, "📦 Phân bổ Biên độ Giảm giá (%)")


def grouped_bar_avg_discount(df: pd.DataFrame) -> go.Figure:
    """Grouped Bar: Mức giảm giá TB theo category_name & brand_type."""
    data = df.groupby(["category_name", "brand_type"])["discount_rate"].mean().reset_index()
    data["discount_pct"] = data["discount_rate"] * 100

    fig = go.Figure()
    for bt in data["brand_type"].unique():
        sub = data[data["brand_type"] == bt].sort_values("discount_pct", ascending=True)
        fig.add_trace(go.Bar(
            y=sub["category_name"],
            x=sub["discount_pct"],
            name=bt,
            orientation="h",
            marker_color=BRAND_COLORS.get(bt, "#999"),
            text=[f"{v:.1f}%" for v in sub["discount_pct"]],
            textposition="outside",
            textfont=dict(size=11, color="#111827"),
            hovertemplate=f"<b>{bt}</b><br>%{{y}}<br>Giảm giá TB: %{{x:.1f}}%<extra></extra>",
        ))
    fig.update_layout(
        barmode="group",
        xaxis_title="Giảm giá trung bình (%)",
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return apply_theme(fig, "📉 Giảm giá TB theo Danh mục sản phẩm")


def render(df: pd.DataFrame):
    """Render toàn bộ MT4."""
    st.markdown("## 🏷️ MT4: Chiến lược Giảm giá — Ai giảm mạnh hơn?")
    st.caption("Phân tích cuộc đua khuyến mãi và mức độ \"cắt máu\" để giành thị phần")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(stacked_bar_discount_flag(df), use_container_width=True)
    with col2:
        st.plotly_chart(boxplot_discount_rate(df), use_container_width=True)

    st.plotly_chart(grouped_bar_avg_discount(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT4", "Hỏi về mức giảm giá, nhãn giảm giá và khác biệt Global vs Local")
