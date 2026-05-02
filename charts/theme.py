"""
theme.py — Bảng màu & Styling thống nhất
Tuân thủ principle.md:
  • Blue–Orange (CVD-friendly)
  • Tối đa 6–12 màu categorical
  • Sequential cho cường độ
  • Highlight / Alert khi cần
"""
import plotly.graph_objects as go

# ── Bảng màu chính ──────────────────────────────────────────────────
BRAND_COLORS = {
    "Global_Brand": "#1565C0",   # Deep Blue
    "Local/OEM":    "#EF6C00",   # Deep Orange (compat)
    "Local/OEM Generic": "#EF6C00",
}

CHANNEL_COLORS = {
    "Tiki Trading": "#00897B",   # Teal
    "Third-Party":  "#8E24AA",   # Purple
}

DISCOUNT_COLORS = {
    "No Discount": "#78909C",    # Blue Grey
    "Normal":      "#FFA726",    # Orange
    "Extreme":     "#E53935",    # Red
}

SUSPECT_COLORS = {
    "Bình thường": "#43A047",    # Green
    "Nghi vấn":   "#E53935",     # Red
}

SALES_COLORS = {
    "Đã bán":  "#1E88E5",       # Blue
    "Chưa bán": "#BDBDBD",      # Grey
}

# ── Bảng màu mở rộng (cho category — tối đa 12) ────────────────────
CATEGORY_PALETTE = [
    "#1565C0", "#EF6C00", "#2E7D32", "#AD1457",
    "#6A1B9A", "#00838F", "#E65100", "#283593",
    "#4E342E", "#558B2F", "#C62828", "#00695C",
]

# ── Sequential palette ──────────────────────────────────────────────
SEQ_BLUE   = ["#E3F2FD", "#90CAF9", "#42A5F5", "#1E88E5", "#1565C0", "#0D47A1"]
SEQ_ORANGE = ["#FFF3E0", "#FFCC80", "#FFA726", "#FB8C00", "#EF6C00", "#E65100"]
DIVERGING  = ["#1565C0", "#64B5F6", "#E0E0E0", "#FFB74D", "#EF6C00"]

# ── Layout mặc định cho mọi biểu đồ ────────────────────────────────
PLOTLY_LAYOUT = dict(
    font=dict(family="Inter, Roboto, sans-serif", size=13, color="#111827"),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=60, r=30, t=50, b=50),
    legend=dict(
        bgcolor="rgba(255,255,255,0.85)",
        bordercolor="rgba(17,24,39,0.12)",
        borderwidth=1,
        font=dict(size=12),
    ),
    hoverlabel=dict(
        bgcolor="rgba(255,255,255,0.98)",
        font_size=13,
        font_family="Inter, sans-serif",
    ),
)

def apply_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Áp dụng theme thống nhất cho figure."""
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=title, font=dict(size=18, color="#111827"), x=0.01),
    )
    # Trục
    fig.update_xaxes(
        gridcolor="rgba(17,24,39,0.08)",
        zerolinecolor="rgba(17,24,39,0.18)",
        tickfont=dict(color="#374151"),
        title_font=dict(color="#111827"),
    )
    fig.update_yaxes(
        gridcolor="rgba(17,24,39,0.08)",
        zerolinecolor="rgba(17,24,39,0.18)",
        tickfont=dict(color="#374151"),
        title_font=dict(color="#111827"),
    )
    return fig


def format_number(n: float) -> str:
    """Format số lớn: 1.2M, 340K, ..."""
    if abs(n) >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    elif abs(n) >= 1_000:
        return f"{n/1_000:.0f}K"
    return f"{n:,.0f}"
