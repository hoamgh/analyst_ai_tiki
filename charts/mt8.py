"""
MT8: Các yếu tố ảnh hưởng Doanh số — Tìm 'điểm bùng phát'
Biểu đồ: Scatter (Review vs Qty), Scatter (Rating vs Qty), Pearson Heatmap
Sử dụng statsmodels OLS regression.
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import streamlit as st
import statsmodels.api as sm
from charts.theme import apply_theme
from stats_engine import correlation_matrix, stepwise_ols_regression, ols_summary_text


def scatter_review_vs_qty(df):
    sub = df[df["quantity_sold"] > 0].copy()
    fig = go.Figure(go.Scattergl(
        x=sub["review_count"], y=sub["quantity_sold"],
        mode="markers",
        marker=dict(size=4, color=sub["rating_average"],
                    colorscale="Viridis", showscale=True,
                    colorbar=dict(title="Rating", tickfont=dict(color="#374151"),
                                  title_font=dict(color="#111827")),
                    opacity=0.6),
        hovertemplate="Review: %{x}<br>Lượng bán: %{y}<br><extra></extra>",
    ))
    fig.update_layout(xaxis_title="Số lượng Review", yaxis_title="Lượng bán",
                      xaxis_type="log", yaxis_type="log")
    fig.add_annotation(text="Trục Log-Log", xref="paper", yref="paper",
                       x=1, y=1, showarrow=False, font=dict(size=11, color="#FFD54F"))
    return apply_theme(fig, "🔬 Tương quan Review vs. Lượng bán")


def scatter_rating_vs_qty(df):
    sub = df[df["quantity_sold"] > 0].copy()
    fig = go.Figure(go.Scattergl(
        x=sub["rating_average"], y=sub["quantity_sold"],
        mode="markers",
        marker=dict(size=4, color="#42A5F5", opacity=0.5),
        hovertemplate="Rating: %{x:.1f}<br>Lượng bán: %{y}<extra></extra>",
    ))
    fig.update_layout(xaxis_title="Rating trung bình", yaxis_title="Lượng bán",
                      yaxis_type="log")
    return apply_theme(fig, "📈 Tương quan Rating vs. Lượng bán")


def pearson_heatmap(df):
    cols = ["price", "rating_average", "review_count", "quantity_sold", "discount_rate"]
    labels = ["Giá", "Rating", "Review", "Lượng bán", "Giảm giá"]
    cm = correlation_matrix(df, cols)
    fig = go.Figure(go.Heatmap(
        z=cm.values, x=labels, y=labels,
        colorscale=[[0,"#E53935"],[0.5,"#EEEEEE"],[1,"#1565C0"]],
        zmin=-1, zmax=1,
        text=[[f"{v:.3f}" for v in row] for row in cm.values],
        texttemplate="%{text}", textfont=dict(size=13, color="#000"),
        hovertemplate="%{y} × %{x}<br>r = %{z:.3f}<extra></extra>",
        colorbar=dict(title="r", tickfont=dict(color="#374151"),
                      title_font=dict(color="#111827")),
    ))
    return apply_theme(fig, "🧮 Ma trận Tương quan Pearson")


def render(df):
    st.markdown("## 📊 MT8: Các yếu tố ảnh hưởng Doanh số — Tìm Điểm bùng phát")
    st.caption("Tìm mối tương quan kỹ thuật giữa các biến số (statsmodels OLS)")
    c1, c2 = st.columns(2)
    with c1: st.plotly_chart(scatter_review_vs_qty(df), use_container_width=True)
    with c2: st.plotly_chart(scatter_rating_vs_qty(df), use_container_width=True)
    st.plotly_chart(pearson_heatmap(df), use_container_width=True)

    # OLS Regression
    with st.expander("📋 Chi tiết Hồi quy OLS (statsmodels)", expanded=False):
        try:
            candidates = ["price", "rating_average", "review_count", "discount_rate"]
            model, selected_cols, crit_value = stepwise_ols_regression(
                df,
                "quantity_sold",
                candidates,
                criterion="aic",
                max_steps=30,
            )
            st.markdown(
                f"**Step-wise OLS (AIC)** — Biến được chọn: `{', '.join(selected_cols) if selected_cols else 'intercept'}`<br>"
                f"**AIC cuối:** `{crit_value:.4f}`",
                unsafe_allow_html=True,
            )
            st.code(ols_summary_text(model), language="text")
            st.markdown(f"**R² = {model.rsquared:.4f}** | "
                        f"**Adj. R² = {model.rsquared_adj:.4f}** | "
                        f"**F-stat = {model.fvalue:.2f}**")
        except Exception as e:
            st.error(f"Lỗi OLS: {e}")

    from ai_section import render_ai_qa
    render_ai_qa(df, "MT8", "Hỏi về tương quan, hồi quy OLS, và yếu tố ảnh hưởng doanh số")
