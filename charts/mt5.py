"""
MT5: Tiki Trading vs. Third-Party — Kênh nào hiệu quả hơn?
Biểu đồ: Bar Charts (so sánh), Violin Plot (Log Scale), Stacked Bar (curation)
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
from charts.theme import CHANNEL_COLORS, BRAND_COLORS, apply_theme, format_number


def bar_channel_comparison(df: pd.DataFrame) -> go.Figure:
    """Bar Charts: Lượng bán TB, Review TB, Rating TB giữa 2 kênh."""
    metrics = {
        "Lượng bán TB": "quantity_sold",
        "Số Review TB":  "review_count",
        "Rating TB":     "rating_average",
    }
    data = df.groupby("channel").agg(
        avg_qty=("quantity_sold", "mean"),
        avg_review=("review_count", "mean"),
        avg_rating=("rating_average", "mean"),
    ).reset_index()

    fig = go.Figure()
    cols = ["avg_qty", "avg_review", "avg_rating"]
    labels = ["Lượng bán TB", "Số Review TB", "Rating TB"]

    from plotly.subplots import make_subplots
    fig = make_subplots(rows=1, cols=3, subplot_titles=labels,
                        horizontal_spacing=0.08)

    for i, (col, label) in enumerate(zip(cols, labels), 1):
        for _, row in data.iterrows():
            ch = row["channel"]
            fig.add_trace(go.Bar(
                x=[ch],
                y=[row[col]],
                name=ch,
                marker_color=CHANNEL_COLORS.get(ch, "#999"),
                text=[f"{row[col]:.1f}"],
                textposition="outside",
                textfont=dict(size=13, color="#111827"),
                showlegend=(i == 1),
                hovertemplate=f"<b>{ch}</b><br>{label}: %{{y:.2f}}<extra></extra>",
            ), row=1, col=i)

    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.08, xanchor="center", x=0.5),
        height=400,
    )
    return apply_theme(fig, "📊 So sánh Hiệu quả: Tiki Trading vs. Third-Party")


def violin_sales(df: pd.DataFrame) -> go.Figure:
    """Violin Plot (Log Scale): Phân tán doanh số theo kênh."""
    fig = go.Figure()
    for ch, color in CHANNEL_COLORS.items():
        sub = df[(df["channel"] == ch) & (df["quantity_sold"] > 0)]["quantity_sold"]
        fig.add_trace(go.Violin(
            y=np.log10(sub + 1),
            name=ch,
            fillcolor=color,
            line_color=color,
            opacity=0.7,
            meanline_visible=True,
            box_visible=True,
            hoverinfo="y+name",
        ))
    fig.update_layout(
        yaxis_title="log₁₀(Lượng bán + 1)",
        showlegend=False,
    )
    fig.add_annotation(
        text="⚠️ Trục Y: Log₁₀ Scale (chỉ SP đã bán)", xref="paper", yref="paper",
        x=1, y=1, showarrow=False,
        font=dict(size=11, color="#FFD54F"),
    )
    return apply_theme(fig, "🎻 Phân tán Doanh số theo Kênh (Violin — Log Scale)")


def stacked_bar_curation(df: pd.DataFrame) -> go.Figure:
    """Stacked Bar: Tỷ lệ SP Tiki Trading theo brand_type (curation strategy)."""
    data = df.groupby(["brand_type", "channel"]).size().reset_index(name="count")
    pivot = data.pivot_table(index="brand_type", columns="channel",
                             values="count", fill_value=0)
    total = pivot.sum(axis=1)
    pct = pivot.div(total, axis=0) * 100

    fig = go.Figure()
    for ch in ["Tiki Trading", "Third-Party"]:
        if ch in pct.columns:
            fig.add_trace(go.Bar(
                x=pct.index,
                y=pct[ch],
                name=ch,
                marker_color=CHANNEL_COLORS.get(ch, "#999"),
                text=[f"{v:.1f}%" for v in pct[ch]],
                textposition="inside",
                textfont=dict(size=13, color="#FFF"),
                hovertemplate=f"<b>{ch}</b><br>%{{x}}<br>Tỷ lệ: %{{y:.1f}}%<extra></extra>",
            ))
    fig.update_layout(
        barmode="stack",
        xaxis_title="Loại thương hiệu",
        yaxis_title="Tỷ lệ (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return apply_theme(fig, "🏪 Tỷ lệ Tiki Trading phân phối theo Brand Type (Curation)")


def render(df: pd.DataFrame):
    """Render toàn bộ MT5."""
    st.markdown("## 🏪 MT5: Tiki Trading vs. Third-Party — Kênh nào hiệu quả hơn?")
    st.caption("Kiểm chứng sức mạnh \"official store\" và hệ sinh thái Tiki")

    st.plotly_chart(bar_channel_comparison(df), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(violin_sales(df), use_container_width=True)
    with col2:
        st.plotly_chart(stacked_bar_curation(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT5", "Hỏi về so sánh hiệu quả kênh, độ phân tán doanh số, chiến lược curation")
