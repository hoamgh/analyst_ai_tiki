"""
MT3: Price Premium — Giá chênh lệch bao nhiêu?
Biểu đồ: Boxplot, Median Price Bar, Heatmap giá trung vị
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
from charts.theme import BRAND_COLORS, SEQ_ORANGE, apply_theme, format_number


def boxplot_price(df: pd.DataFrame) -> go.Figure:
    """Boxplot: Phân bổ dải giá của Global vs Local."""
    fig = go.Figure()
    for bt, color in BRAND_COLORS.items():
        sub = df[df["brand_type"] == bt]["price"]
        fig.add_trace(go.Box(
            y=sub,
            name=bt,
            marker_color=color,
            line_color=color,
            boxmean="sd",
            hoverinfo="y+name",
        ))
    fig.update_layout(
        yaxis_title="Giá (VNĐ)",
        yaxis_type="log",
        showlegend=False,
    )
    fig.add_annotation(
        text="⚠️ Trục Y: Log Scale", xref="paper", yref="paper",
        x=1, y=1, showarrow=False,
        font=dict(size=11, color="#FFD54F"),
    )
    return apply_theme(fig, "📦 Phân bổ Dải giá — Global vs. Local (Boxplot)")


def median_price_bar(df: pd.DataFrame) -> go.Figure:
    """Median Price Bar: Giá trung vị theo category_name & brand_type."""
    data = df.groupby(["category_name", "brand_type"])["price"].median().reset_index()
    pivot = data.pivot_table(index="category_name", columns="brand_type",
                             values="price", fill_value=0)

    fig = go.Figure()
    for bt in pivot.columns:
        fig.add_trace(go.Bar(
            y=pivot.index,
            x=pivot[bt],
            name=bt,
            orientation="h",
            marker_color=BRAND_COLORS.get(bt, "#999"),
            text=[format_number(v) for v in pivot[bt]],
            textposition="outside",
            textfont=dict(size=11, color="#111827"),
            hovertemplate=f"<b>{bt}</b><br>%{{y}}<br>Giá trung vị: %{{x:,.0f}} VNĐ<extra></extra>",
        ))
    fig.update_layout(
        barmode="group",
        xaxis_title="Giá trung vị (VNĐ)",
        yaxis_title="",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    fig.update_yaxes(autorange="reversed")
    return apply_theme(fig, "💰 Giá trung vị theo Danh mục — So sánh Brand")


def heatmap_median_price(df: pd.DataFrame) -> go.Figure:
    """Heatmap: Giá trung vị giữa category_name x brand_type."""
    data = df.groupby(["category_name", "brand_type"])["price"].median().reset_index()
    pivot = data.pivot_table(index="category_name", columns="brand_type",
                             values="price", fill_value=0)

    # Tính ratio (Global / Local) để tìm điểm nóng
    text_vals = pivot.values.copy().astype(float)
    display_text = [[format_number(v) for v in row] for row in text_vals]

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#1565C0"], [0.3, "#42A5F5"], [0.5, "#E0E0E0"],
                     [0.7, "#FFA726"], [1, "#E65100"]],
        text=display_text,
        texttemplate="%{text}",
        textfont=dict(size=12, color="#FFF"),
        hovertemplate="<b>%{y}</b> × %{x}<br>Giá trung vị: %{z:,.0f} VNĐ<extra></extra>",
        colorbar=dict(title="VNĐ", tickfont=dict(color="#374151"),
                  title_font=dict(color="#111827")),
    ))
    fig.update_layout(xaxis_title="Loại thương hiệu", yaxis_title="")
    fig.update_yaxes(autorange="reversed")
    return apply_theme(fig, "🔥 Heatmap Giá trung vị — Điểm nóng Premium")


def render(df: pd.DataFrame):
    """Render toàn bộ MT3."""
    st.markdown("## 💎 MT3: Price Premium — Giá chênh lệch bao nhiêu?")
    st.caption("Đo lường quyền lực định giá và \"phí thương hiệu\" (Brand Premium)")

    st.plotly_chart(boxplot_price(df), use_container_width=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(median_price_bar(df), use_container_width=True)
    with col2:
        st.plotly_chart(heatmap_median_price(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT3", "Hỏi về chênh lệch giá, brand premium theo danh mục")
