"""
MT2: Phân khúc Thị trường — Ai thống lĩnh vùng giá nào?
Biểu đồ: 100% Stacked Bar, Clustered Bar, Heatmap (Density)
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from charts.theme import (
    BRAND_COLORS, CATEGORY_PALETTE, SEQ_BLUE, apply_theme, format_number
)

SEGMENT_ORDER = ["Dưới 100K", "100K – 500K", "500K – 2M", "2M – 5M", "Trên 5M"]


def stacked_bar_segment(df: pd.DataFrame) -> go.Figure:
    """100% Stacked Bar: Tỷ lệ lượng bán Global vs Local trong 5 phân khúc giá."""
    data = df.groupby(["price_segment", "brand_type"], observed=False)["quantity_sold"].sum().reset_index()
    pivot = data.pivot_table(
        index="price_segment",
        columns="brand_type",
        values="quantity_sold",
        fill_value=0,
        observed=False,
    )
    pivot = pivot.reindex(SEGMENT_ORDER)
    total = pivot.sum(axis=1)
    pct = pivot.div(total, axis=0) * 100

    fig = go.Figure()
    for bt in pct.columns:
        fig.add_trace(go.Bar(
            x=pct.index.astype(str),
            y=pct[bt],
            name=bt,
            marker_color=BRAND_COLORS.get(bt, "#999"),
            text=[f"{v:.1f}%" for v in pct[bt]],
            textposition="inside",
            textfont=dict(size=12, color="#FFF"),
            hovertemplate=f"<b>{bt}</b><br>Phân khúc: %{{x}}<br>Tỷ lệ: %{{y:.1f}}%<extra></extra>",
        ))
    fig.update_layout(barmode="stack", xaxis_title="Phân khúc giá", yaxis_title="Tỷ lệ (%)")
    return apply_theme(fig, "📊 Tỷ lệ lượng bán theo Phân khúc giá (100% Stacked)")


def clustered_bar_segment(df: pd.DataFrame) -> go.Figure:
    """Clustered Bar: Tổng lượng bán theo dải giá — tìm 'điểm rơi'."""
    data = df.groupby("price_segment", observed=False)["quantity_sold"].sum().reset_index()
    data["price_segment"] = pd.Categorical(data["price_segment"], categories=SEGMENT_ORDER, ordered=True)
    data = data.sort_values("price_segment")

    # Highlight phân khúc cao nhất
    max_idx = data["quantity_sold"].idxmax()
    colors = ["#FFD54F" if i == max_idx else "#42A5F5" for i in data.index]

    fig = go.Figure(go.Bar(
        x=data["price_segment"].astype(str),
        y=data["quantity_sold"],
        marker_color=colors,
        text=[format_number(v) for v in data["quantity_sold"]],
        textposition="outside",
        textfont=dict(size=13, color="#111827"),
        hovertemplate="<b>%{x}</b><br>Lượng bán: %{y:,.0f}<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Phân khúc giá", yaxis_title="Tổng lượng bán")
    # Annotate highlight
    max_seg = data.loc[max_idx, "price_segment"]
    fig.add_annotation(
        x=str(max_seg), y=data.loc[max_idx, "quantity_sold"],
        text="🎯 Điểm rơi", showarrow=True,
        arrowhead=2, arrowcolor="#FFD54F",
        font=dict(size=14, color="#FFD54F"), yshift=25,
    )
    return apply_theme(fig, "📉 Tổng lượng bán theo Phân khúc giá — Tìm Điểm rơi")


def heatmap_density(df: pd.DataFrame) -> go.Figure:
    """Heatmap: Mật độ phân bổ sản phẩm theo Ngành hàng x Dải giá."""
    data = df.groupby(["category_name", "price_segment"], observed=False).size().reset_index(name="count")
    pivot = data.pivot_table(
        index="category_name",
        columns="price_segment",
        values="count",
        fill_value=0,
        observed=False,
    )
    pivot = pivot.reindex(columns=SEGMENT_ORDER)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, "#0D47A1"], [0.25, "#1565C0"], [0.5, "#42A5F5"],
                     [0.75, "#FFA726"], [1, "#E65100"]],
        text=pivot.values,
        texttemplate="%{text}",
        textfont=dict(size=11, color="#FFF"),
        hovertemplate="<b>%{y}</b> × %{x}<br>Số SP: %{z}<extra></extra>",
        colorbar=dict(title="Số SP", tickfont=dict(color="#374151"),
                  title_font=dict(color="#111827")),
    ))
    fig.update_layout(xaxis_title="Phân khúc giá", yaxis_title="")
    fig.update_yaxes(autorange="reversed")
    return apply_theme(fig, "🔥 Mật độ sản phẩm: Ngành hàng × Dải giá")


def render(df: pd.DataFrame):
    """Render toàn bộ MT2."""
    st.markdown("## 🗺️ MT2: Phân khúc Thị trường — Ai thống lĩnh vùng giá nào?")
    st.caption("Xác định \"vùng xanh\" và \"vùng đỏ\" cạnh tranh theo các dải giá")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(stacked_bar_segment(df), use_container_width=True)
    with col2:
        st.plotly_chart(clustered_bar_segment(df), use_container_width=True)

    st.plotly_chart(heatmap_density(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT2", "Hỏi về phân khúc giá, điểm rơi thị trường, mật độ ngành hàng")
