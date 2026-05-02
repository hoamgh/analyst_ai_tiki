"""
MT7: Độ tin cậy hệ thống Đánh giá — Bóc tách Rating nghi vấn
Biểu đồ: Heatmap-style Bar, Comparative Bar, 100% Stacked Bar
"""
import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from charts.theme import BRAND_COLORS, SUSPECT_COLORS, apply_theme


def heatmap_bar_suspect_by_category(df):
    data = df.groupby("category_name")["is_rating_suspect"].mean().reset_index()
    data.columns = ["category_name", "suspect_pct"]
    data["suspect_pct"] = (data["suspect_pct"] * 100).round(1)
    data = data.sort_values("suspect_pct", ascending=True)
    max_p, min_p = data["suspect_pct"].max(), data["suspect_pct"].min()
    rng = max_p - min_p if max_p != min_p else 1
    colors = []
    for v in data["suspect_pct"]:
        r = (v - min_p) / rng
        colors.append(f"rgb({int(67+162*r)},{int(160-103*r)},{int(71-18*r)})")
    fig = go.Figure(go.Bar(
        y=data["category_name"], x=data["suspect_pct"], orientation="h",
        marker_color=colors,
        text=[f"{v:.1f}%" for v in data["suspect_pct"]],
        textposition="outside", textfont=dict(size=12, color="#111827"),
        hovertemplate="<b>%{y}</b><br>% Nghi vấn: %{x:.1f}%<extra></extra>",
    ))
    fig.update_layout(xaxis_title="% SP Rating nghi vấn", yaxis_title="")
    return apply_theme(fig, "🔥 Xếp hạng % Rating Nghi vấn theo Danh mục")


def comparative_bar_rating(df):
    data = df.groupby("suspect_label")["rating_average"].mean().reset_index()
    fig = go.Figure()
    for _, row in data.iterrows():
        lb = row["suspect_label"]
        fig.add_trace(go.Bar(x=[lb], y=[row["rating_average"]], name=lb,
            marker_color=SUSPECT_COLORS.get(lb, "#999"),
            text=[f"{row['rating_average']:.2f}"], textposition="outside",
            textfont=dict(size=16, color="#111827"), width=0.4))
    fig.update_layout(yaxis_title="Rating TB", showlegend=False, yaxis_range=[0,5.2])
    fig.add_hline(y=4.5, line_dash="dot", line_color="#FFD54F",
                  annotation_text="Ngưỡng 4.5", annotation_font=dict(size=12, color="#FFD54F"))
    return apply_theme(fig, "⚖️ Rating TB: Bình thường vs. Nghi vấn")


def stacked_bar_suspect_brand(df):
    data = df.groupby(["brand_type","suspect_label"]).size().reset_index(name="count")
    pivot = data.pivot_table(index="brand_type", columns="suspect_label", values="count", fill_value=0)
    total = pivot.sum(axis=1)
    pct = pivot.div(total, axis=0) * 100
    fig = go.Figure()
    for lb in ["Bình thường","Nghi vấn"]:
        if lb in pct.columns:
            fig.add_trace(go.Bar(x=pct.index, y=pct[lb], name=lb,
                marker_color=SUSPECT_COLORS.get(lb,"#999"),
                text=[f"{v:.1f}%" for v in pct[lb]], textposition="inside",
                textfont=dict(size=13, color="#FFF")))
    fig.update_layout(barmode="stack", xaxis_title="Loại thương hiệu", yaxis_title="Tỷ lệ (%)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5))
    return apply_theme(fig, "📊 Tỷ trọng SP Nghi vấn: Global vs. Local")


def render(df):
    st.markdown("## 🔍 MT7: Độ tin cậy Rating — Bóc tách Rating nghi vấn")
    st.caption("Nhận diện thủ thuật \"buff rating\" và niềm tin ảo (Rating > 4.5, Review < 10)")
    total = len(df)
    sus = int(df["is_rating_suspect"].sum())
    k1, k2, k3 = st.columns(3)
    k1.metric("Tổng SP", f"{total:,}")
    k2.metric("SP Nghi vấn", f"{sus:,}", f"{sus/total*100:.1f}%")
    k3.metric("SP Bình thường", f"{total-sus:,}")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(comparative_bar_rating(df), use_container_width=True)
    with c2: st.plotly_chart(stacked_bar_suspect_brand(df), use_container_width=True)
    st.plotly_chart(heatmap_bar_suspect_by_category(df), use_container_width=True)

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT7", "Hỏi về mức độ nghi vấn rating, danh mục rủi ro, tác động tới niềm tin")
