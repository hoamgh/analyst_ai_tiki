"""
MT1: Thị phần Doanh số — Ai bán nhiều nhất?
Biểu đồ: Donut, Pie, 100% Stacked Bar, Combo (Bar + Line)
"""
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import streamlit as st
from charts.theme import (
    BRAND_COLORS, CATEGORY_PALETTE, apply_theme, format_number
)


def donut_quantity_sold(df: pd.DataFrame) -> go.Figure:
    """Donut Chart: Tỷ lệ % tổng lượng bán theo brand_type."""
    data = df.groupby("brand_type")["quantity_sold"].sum().reset_index()
    colors = [BRAND_COLORS.get(b, "#999") for b in data["brand_type"]]
    fig = go.Figure(go.Pie(
        labels=data["brand_type"],
        values=data["quantity_sold"],
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#1e1e2e", width=2)),
        textinfo="label+percent",
        textfont=dict(size=14, color="#FFF"),
        hovertemplate="<b>%{label}</b><br>Lượng bán: %{value:,.0f}<br>Tỷ lệ: %{percent}<extra></extra>",
    ))
    # Annotation trung tâm
    total = data["quantity_sold"].sum()
    fig.add_annotation(
        text=f"<b>{format_number(total)}</b><br><span style='font-size:11px'>Tổng lượng bán</span>",
        showarrow=False, font=dict(size=16, color="#111827"),
    )
    return apply_theme(fig, "🍩 Tỷ lệ Tổng lượng bán theo Loại thương hiệu")


def pie_product_count(df: pd.DataFrame) -> go.Figure:
    """Pie Chart: Tỷ lệ % số lượng mẫu mã theo brand_type."""
    data = df.groupby("brand_type")["product_id"].nunique().reset_index(name="count")
    colors = [BRAND_COLORS.get(b, "#999") for b in data["brand_type"]]
    fig = go.Figure(go.Pie(
        labels=data["brand_type"],
        values=data["count"],
        marker=dict(colors=colors, line=dict(color="#1e1e2e", width=2)),
        textinfo="label+percent",
        textfont=dict(size=14, color="#FFF"),
        hovertemplate="<b>%{label}</b><br>Số mẫu mã: %{value:,.0f}<br>Tỷ lệ: %{percent}<extra></extra>",
    ))
    return apply_theme(fig, "🥧 Tỷ lệ Số lượng mẫu mã theo Loại thương hiệu")


def stacked_bar_revenue_by_category(df: pd.DataFrame) -> go.Figure:
    """100% Stacked Bar: Phân rã thị phần doanh thu theo category_name."""
    data = df.groupby(["category_name", "brand_type"])["revenue"].sum().reset_index()
    pivot = data.pivot_table(index="category_name", columns="brand_type", values="revenue", fill_value=0)
    # Tính tỷ lệ %
    total = pivot.sum(axis=1)
    pct = pivot.div(total, axis=0) * 100

    fig = go.Figure()
    for bt in pct.columns:
        fig.add_trace(go.Bar(
            y=pct.index,
            x=pct[bt],
            name=bt,
            orientation="h",
            marker_color=BRAND_COLORS.get(bt, "#999"),
            text=[f"{v:.1f}%" for v in pct[bt]],
            textposition="inside",
            textfont=dict(size=11, color="#FFF"),
            hovertemplate=f"<b>{bt}</b><br>Danh mục: %{{y}}<br>Tỷ lệ: %{{x:.1f}}%<extra></extra>",
        ))

    fig.update_layout(barmode="stack", xaxis_title="Tỷ lệ doanh thu (%)", yaxis_title="")
    fig.update_yaxes(autorange="reversed")
    return apply_theme(fig, "📊 Thị phần doanh thu theo Danh mục (100% Stacked)")


def combo_total_vs_avg(df: pd.DataFrame) -> go.Figure:
    """Combo Chart: Tổng lượng bán (Bar) + Trung bình lượng bán/SP (Line)."""
    data = df.groupby("brand_type").agg(
        total_qty=("quantity_sold", "sum"),
        product_count=("product_id", "nunique"),
    ).reset_index()
    data["avg_qty"] = data["total_qty"] / data["product_count"]

    fig = go.Figure()
    # Bar — Tổng lượng bán
    fig.add_trace(go.Bar(
        x=data["brand_type"],
        y=data["total_qty"],
        name="Tổng lượng bán",
        marker_color=[BRAND_COLORS.get(b, "#999") for b in data["brand_type"]],
        text=[format_number(v) for v in data["total_qty"]],
        textposition="outside",
        textfont=dict(size=13, color="#111827"),
        yaxis="y",
    ))
    # Line — Avg Qty Per Product
    fig.add_trace(go.Scatter(
        x=data["brand_type"],
        y=data["avg_qty"],
        name="TB lượng bán / SP",
        mode="lines+markers+text",
        line=dict(color="#FFD54F", width=3),
        marker=dict(size=10, color="#FFD54F", line=dict(color="#FFF", width=2)),
        text=[f"{v:.1f}" for v in data["avg_qty"]],
        textposition="top center",
        textfont=dict(size=13, color="#FFD54F"),
        yaxis="y2",
    ))

    fig.update_layout(
        yaxis=dict(title="Tổng lượng bán", side="left"),
        yaxis2=dict(title="TB lượng bán / SP", overlaying="y", side="right",
                    showgrid=False, tickfont=dict(color="#FFD54F"),
                    title_font=dict(color="#FFD54F")),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return apply_theme(fig, "📈 Tổng lượng bán vs. Trung bình / Sản phẩm")


def render(df: pd.DataFrame):
    """Render toàn bộ MT1."""
    st.markdown("## 🏆 MT1: Thị phần Doanh số — Ai bán nhiều nhất?")
    st.caption("So sánh \"Số lượng mẫu mã\" và \"Hiệu quả thực tế\" của Global Brand vs. Local/OEM")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(donut_quantity_sold(df), use_container_width=True)
    with col2:
        st.plotly_chart(pie_product_count(df), use_container_width=True)

    st.plotly_chart(stacked_bar_revenue_by_category(df), use_container_width=True)
    st.plotly_chart(combo_total_vs_avg(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT1", "Hỏi về thị phần doanh số, số mẫu mã, hiệu quả Global vs Local")
