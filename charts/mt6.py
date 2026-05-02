"""
MT6: Tỷ lệ Chuyển đổi — Brand nào dễ bán hơn?
Biểu đồ: 100% Stacked Bar, Matrix Heatmap, Horizontal Bar (ranking)
"""
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from charts.theme import (
    BRAND_COLORS, SALES_COLORS, CHANNEL_COLORS, apply_theme, format_number
)


def stacked_bar_conversion(df: pd.DataFrame) -> go.Figure:
    """100% Stacked Bar: Tỷ lệ 'Đã bán' vs 'Chưa bán' theo brand_type."""
    data = df.groupby(["brand_type", "has_sales"]).size().reset_index(name="count")
    pivot = data.pivot_table(index="brand_type", columns="has_sales",
                             values="count", fill_value=0)
    total = pivot.sum(axis=1)
    pct = pivot.div(total, axis=0) * 100

    fig = go.Figure()
    for status in ["Đã bán", "Chưa bán"]:
        if status in pct.columns:
            fig.add_trace(go.Bar(
                x=pct.index,
                y=pct[status],
                name=status,
                marker_color=SALES_COLORS.get(status, "#999"),
                text=[f"{v:.1f}%" for v in pct[status]],
                textposition="inside",
                textfont=dict(size=14, color="#FFF" if status == "Đã bán" else "#333"),
                hovertemplate=f"<b>{status}</b><br>%{{x}}<br>Tỷ lệ: %{{y:.1f}}%<extra></extra>",
            ))
    fig.update_layout(
        barmode="stack",
        xaxis_title="Loại thương hiệu",
        yaxis_title="Tỷ lệ (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return apply_theme(fig, "📊 Tỷ lệ Chuyển đổi: Đã bán vs. Chưa bán")


def heatmap_conversion_matrix(df: pd.DataFrame) -> go.Figure:
    """Matrix Heatmap: Tỷ lệ chuyển đổi Brand × Kênh."""
    total = df.groupby(["brand_type", "channel"]).size().reset_index(name="total")
    sold = df[df["quantity_sold"] > 0].groupby(["brand_type", "channel"]).size().reset_index(name="sold")
    merged = total.merge(sold, on=["brand_type", "channel"], how="left").fillna(0)
    merged["conv_rate"] = (merged["sold"] / merged["total"] * 100).round(1)

    pivot = merged.pivot_table(index="brand_type", columns="channel",
                               values="conv_rate", fill_value=0)

    fig = go.Figure(go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale=[[0, "#E53935"], [0.5, "#FFD54F"], [1, "#43A047"]],
        text=[[f"{v:.1f}%" for v in row] for row in pivot.values],
        texttemplate="%{text}",
        textfont=dict(size=16, color="#FFF"),
        hovertemplate="<b>%{y}</b> × %{x}<br>Tỷ lệ chuyển đổi: %{z:.1f}%<extra></extra>",
        colorbar=dict(title="%", tickfont=dict(color="#374151"),
                  title_font=dict(color="#111827")),
    ))
    fig.update_layout(xaxis_title="Kênh phân phối", yaxis_title="")
    return apply_theme(fig, "🧩 Ma trận Chuyển đổi: Brand × Kênh")


def horizontal_bar_category_conversion(df: pd.DataFrame) -> go.Figure:
    """Horizontal Bar: Xếp hạng tỷ lệ chuyển đổi theo danh mục."""
    total = df.groupby("category_name").size().rename("total")
    sold = df[df["quantity_sold"] > 0].groupby("category_name").size().rename("sold")
    result = pd.concat([total, sold], axis=1).fillna(0)
    result["conv_rate"] = (result["sold"] / result["total"] * 100).round(1)
    result = result.sort_values("conv_rate", ascending=True).reset_index()

    # Color gradient: low → red, high → green
    max_rate = result["conv_rate"].max()
    min_rate = result["conv_rate"].min()
    range_rate = max_rate - min_rate if max_rate != min_rate else 1
    colors = []
    for v in result["conv_rate"]:
        ratio = (v - min_rate) / range_rate
        if ratio < 0.5:
            colors.append(f"rgba(229, 57, 53, {0.5 + ratio})")
        else:
            colors.append(f"rgba(67, 160, 71, {ratio})")

    fig = go.Figure(go.Bar(
        y=result["category_name"],
        x=result["conv_rate"],
        orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}%" for v in result["conv_rate"]],
        textposition="outside",
        textfont=dict(size=12, color="#111827"),
        hovertemplate="<b>%{y}</b><br>Tỷ lệ chuyển đổi: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Tỷ lệ chuyển đổi (%)", yaxis_title="")
    return apply_theme(fig, "🏅 Xếp hạng Tỷ lệ Chuyển đổi theo Danh mục")


def render(df: pd.DataFrame):
    """Render toàn bộ MT6."""
    st.markdown("## 🎯 MT6: Tỷ lệ Chuyển đổi — Brand nào dễ bán hơn?")
    st.caption("Tìm \"tấm vé thông hành\" giúp sản phẩm mới thoát khỏi tình trạng không đơn hàng")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(stacked_bar_conversion(df), use_container_width=True)
    with col2:
        st.plotly_chart(heatmap_conversion_matrix(df), use_container_width=True)

    st.plotly_chart(horizontal_bar_category_conversion(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT6", "Hỏi về tỷ lệ chuyển đổi theo brand/kênh/danh mục và ý nghĩa chiến lược")
