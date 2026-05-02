"""
ai_section.py — Component AI Q&A dùng chung cho mọi MT
Mỗi MT sẽ gọi render_ai_qa() ở cuối để hiển thị ô hỏi AI riêng.
"""
import streamlit as st
from stats_engine import build_context_for_mt
from gemini_helper import ask_gemini
from log_helper import log_interaction


@st.cache_data(show_spinner=False)
def _get_cached_context(df, mt_code: str) -> str:
    """Cache System Context theo (df sau lọc, mt_code) để hỏi AI nhanh hơn."""
    return build_context_for_mt(df, mt_code)


def render_ai_qa(df, mt_code: str, chart_description: str = ""):
    """
    Render ô hỏi AI riêng cho mỗi mục tiêu phân tích.
    Mỗi MT có key riêng biệt để tránh xung đột widget.
    """
    st.markdown("---")
    st.markdown(f"### 🤖 Hỏi AI về {mt_code}")
    if chart_description:
        st.caption(chart_description)

    user_query = st.text_input(
        "💬 Câu hỏi của bạn:",
        placeholder=f"Ví dụ: Phân tích xu hướng chính trong {mt_code}...",
        key=f"ai_query_{mt_code}",
    )

    if st.button("🚀 Gửi câu hỏi", type="primary", use_container_width=True,
                 key=f"ai_btn_{mt_code}"):
        if user_query.strip():
            with st.spinner("🔄 Đang phân tích dữ liệu và sinh nhận xét…"):
                # Bước 1 & 2: Trích xuất + Đóng gói ngữ cảnh
                system_ctx = _get_cached_context(df, mt_code)
                # Bước 3: Gọi Gemini
                ai_response = ask_gemini(system_ctx, user_query, mt_code)
                # Bước 4: Lưu vết
                log_interaction(mt_code, user_query, system_ctx, ai_response)

            st.markdown(ai_response)

            with st.expander("📄 Xem System Context đã gửi cho AI", expanded=False):
                st.code(system_ctx, language="markdown")
        else:
            st.warning("Vui lòng nhập câu hỏi.")
