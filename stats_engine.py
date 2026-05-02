"""
stats_engine.py — Tầng Xử lý thống kê
Sử dụng statsmodels + pandas để cung cấp kết quả phân tích kỹ thuật.
"""
import pandas as pd
import numpy as np
import statsmodels.api as sm


def _brand_type_from_query(q: str) -> str | None:
    q = q.lower()
    if "global" in q:
        return "Global_Brand"
    if "local" in q or "oem" in q or "generic" in q or "địa phương" in q:
        return "Local/OEM Generic"
    return None


def _append_price_by_category(ctx_parts: list[str], df: pd.DataFrame, brand_type: str | None = None, top_n: int = 12):
    """Bảng giá theo danh mục (median) — có thể lọc theo brand_type."""
    if "category_name" not in df.columns or "price" not in df.columns:
        return

    sub = df
    title_suffix = ""
    if brand_type and "brand_type" in df.columns:
        sub = df[df["brand_type"] == brand_type]
        title_suffix = f" (chỉ {brand_type})"

    if len(sub) == 0:
        return

    tbl = (
        sub.groupby("category_name", observed=False)["price"]
        .median()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="median_price")
    )
    ctx_parts.append(f"Giá trung vị theo danh mục{title_suffix} (Top {top_n}):")
    ctx_parts.append(tbl.to_markdown(index=False))


def _append_price_segment_by_category(ctx_parts: list[str], df: pd.DataFrame, brand_type: str | None = None, top_n: int = 20):
    """Bảng median price theo (category × price_segment) để trả lời câu hỏi liên quan phân khúc."""
    if not all(c in df.columns for c in ["category_name", "price_segment", "price"]):
        return
    sub = df
    title_suffix = ""
    if brand_type and "brand_type" in df.columns:
        sub = df[df["brand_type"] == brand_type]
        title_suffix = f" (chỉ {brand_type})"
    if len(sub) == 0:
        return

    tbl = (
        sub.groupby(["category_name", "price_segment"], observed=False)["price"]
        .median()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index(name="median_price")
    )
    ctx_parts.append(f"Giá trung vị theo Danh mục × Phân khúc giá{title_suffix} (Top {top_n} dòng):")
    ctx_parts.append(tbl.to_markdown(index=False))


def descriptive_stats(df: pd.DataFrame, columns: list[str] | None = None) -> str:
    """Trả về bảng describe() dạng chuỗi markdown."""
    if columns:
        desc = df[columns].describe()
    else:
        desc = df.describe()
    return desc.to_markdown()


def correlation_matrix(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    """Ma trận tương quan Pearson."""
    return df[cols].corr(method="pearson")


def ols_regression(df: pd.DataFrame, y_col: str, x_cols: list[str]) -> sm.regression.linear_model.RegressionResultsWrapper:
    """Hồi quy OLS: y ~ x1 + x2 + ..."""
    # Giải thích tự nhiên: Đoạn code này sẽ loại bỏ các dòng bị thiếu dữ liệu
    # ở bất kỳ cột nào trong (y_col + x_cols) bằng hàm dropna() của Pandas,
    # nhằm đảm bảo mô hình OLS chỉ học trên các quan sát đầy đủ.
    subset = df[[y_col] + x_cols].dropna()
    X = sm.add_constant(subset[x_cols].astype(float))
    y = subset[y_col].astype(float)
    model = sm.OLS(y, X).fit()
    return model


def stepwise_ols_regression(
    df: pd.DataFrame,
    y_col: str,
    candidate_x_cols: list[str],
    *,
    criterion: str = "aic",
    max_steps: int = 30,
):
    """Step-wise OLS (forward + backward) để chọn biến giải thích.

    Giải thích tự nhiên: Đoạn code này sẽ tự động thử thêm/bớt từng biến trong danh sách
    candidate_x_cols và chọn tập biến làm mô hình tốt hơn theo tiêu chí AIC/BIC.
    Mục tiêu là tránh “chọn biến bằng tay” và hạn chế mô hình quá nhiều biến.

    Lưu ý minh bạch:
    - Chỉ chạy khi được gọi (người dùng mở MT8/expander), không chạy âm thầm.
    - Không thay đổi dữ liệu gốc; mọi tính toán trên DataFrame trong RAM.
    """

    crit = (criterion or "aic").strip().lower()
    if crit not in {"aic", "bic"}:
        raise ValueError("criterion must be 'aic' or 'bic'")

    # Dùng cùng một tập dòng (dropna theo toàn bộ candidate) để các mô hình so sánh công bằng.
    cols_needed = [y_col] + [c for c in candidate_x_cols if c in df.columns]
    subset = df[cols_needed].dropna()
    if len(subset) == 0:
        raise ValueError("No rows available after dropna for step-wise OLS")

    def _fit(x_cols: list[str]):
        X = subset[x_cols].astype(float) if x_cols else pd.DataFrame(index=subset.index)
        X = sm.add_constant(X, has_constant="add")
        y = subset[y_col].astype(float)
        return sm.OLS(y, X).fit()

    def _score(model):
        return float(model.aic if crit == "aic" else model.bic)

    remaining = [c for c in candidate_x_cols if c in subset.columns and c != y_col]
    selected: list[str] = []

    best_model = _fit(selected)
    best_score = _score(best_model)

    for _ in range(max_steps):
        improved = False

        # Forward step: thử thêm từng biến chưa chọn
        forward_best = None
        forward_best_col = None
        forward_best_score = best_score
        for col in remaining:
            try:
                m = _fit(selected + [col])
                s = _score(m)
            except Exception:
                continue
            if s < forward_best_score - 1e-6:
                forward_best = m
                forward_best_col = col
                forward_best_score = s

        if forward_best is not None and forward_best_col is not None:
            selected.append(forward_best_col)
            remaining.remove(forward_best_col)
            best_model = forward_best
            best_score = forward_best_score
            improved = True

        # Backward step: thử bỏ từng biến đang chọn
        backward_best = None
        backward_best_col = None
        backward_best_score = best_score
        if selected:
            for col in list(selected):
                try:
                    trial = [c for c in selected if c != col]
                    m = _fit(trial)
                    s = _score(m)
                except Exception:
                    continue
                if s < backward_best_score - 1e-6:
                    backward_best = m
                    backward_best_col = col
                    backward_best_score = s

        if backward_best is not None and backward_best_col is not None:
            selected.remove(backward_best_col)
            remaining.append(backward_best_col)
            best_model = backward_best
            best_score = backward_best_score
            improved = True

        if not improved:
            break

    return best_model, selected, best_score


def ols_summary_text(model) -> str:
    """Trích xuất bản tóm tắt OLS dạng text."""
    return model.summary().as_text()


def group_stats(df: pd.DataFrame, group_col: str, value_col: str) -> pd.DataFrame:
    """Thống kê theo nhóm: count, mean, median, std, sum."""
    return df.groupby(group_col)[value_col].agg(
        ["count", "mean", "median", "std", "sum"]
    ).reset_index()


def suspect_rating_stats(df: pd.DataFrame) -> dict:
    """Thống kê sản phẩm rating nghi vấn."""
    total = len(df)
    suspect = df["is_rating_suspect"].sum()
    pct = round(suspect / total * 100, 2) if total > 0 else 0
    avg_normal = df.loc[df["is_rating_suspect"] == 0, "rating_average"].mean()
    avg_suspect = df.loc[df["is_rating_suspect"] == 1, "rating_average"].mean()
    return {
        "total_products": total,
        "suspect_count": int(suspect),
        "suspect_pct": pct,
        "avg_rating_normal": round(avg_normal, 3) if not pd.isna(avg_normal) else 0,
        "avg_rating_suspect": round(avg_suspect, 3) if not pd.isna(avg_suspect) else 0,
    }


def conversion_rate(df: pd.DataFrame, group_col: str) -> pd.DataFrame:
    """Tỷ lệ chuyển đổi (% đã bán) theo nhóm."""
    total = df.groupby(group_col).size().rename("total")
    sold = df[df["quantity_sold"] > 0].groupby(group_col).size().rename("sold")
    result = pd.concat([total, sold], axis=1).fillna(0)
    result["conversion_rate"] = round(result["sold"] / result["total"] * 100, 2)
    return result.reset_index()


def price_premium_stats(df: pd.DataFrame) -> str:
    """Thống kê price premium giữa Global vs Local."""
    stats_list = []
    for bt in df["brand_type"].unique():
        sub = df[df["brand_type"] == bt]["price"]
        stats_list.append({
            "brand_type": bt,
            "median_price": sub.median(),
            "mean_price": sub.mean(),
            "std_price": sub.std(),
            "min_price": sub.min(),
            "max_price": sub.max(),
        })
    return pd.DataFrame(stats_list).to_markdown(index=False)


def build_context_for_mt(df: pd.DataFrame, mt_code: str) -> str:
    """
    Xây dựng System Context (chuỗi văn bản thống kê) cho một mục tiêu.
    Tuân thủ pre-analyst.md: chỉ gửi text, KHÔNG gửi hình ảnh.
    """
    ctx_parts = [f"[BẢN TIN PHÂN TÍCH DỮ LIỆU TIKI — {mt_code}]"]
    ctx_parts.append(f"Tổng sản phẩm (sau lọc): {len(df)}")
    if "category_name" in df.columns:
        ctx_parts.append(f"Số danh mục (sau lọc): {df['category_name'].nunique()}")
    if "brand_type" in df.columns:
        ctx_parts.append(f"brand_type có trong dữ liệu: {sorted(df['brand_type'].dropna().unique().tolist())}")

    ctx_parts.append("--- Định nghĩa biến/metric (để tránh hiểu sai) ---")
    ctx_parts.append("- revenue = price * quantity_sold (doanh thu ước tính)")
    ctx_parts.append("- quantity_sold: tổng lượng bán (đơn vị sản phẩm)")
    ctx_parts.append("- category_name: danh mục sản phẩm")

    # Giúp AI biết rõ dữ liệu đang có cột gì (tránh trả lời nhầm kiểu 'không có danh mục')
    ctx_parts.append("--- Cột dữ liệu hiện có ---")
    ctx_parts.append(", ".join(sorted([str(c) for c in df.columns])))

    if mt_code == "MT1":
        ctx_parts.append("--- Thị phần Doanh số ---")
        # Số mẫu mã (đúng với Pie chart trong MT1)
        if "product_id" in df.columns:
            prod = (
                df.groupby("brand_type", observed=False)["product_id"]
                .nunique()
                .reset_index(name="product_count")
            )
            ctx_parts.append("Số lượng mẫu mã (unique product_id) theo brand_type:")
            ctx_parts.append(prod.to_markdown(index=False))

        gs = group_stats(df, "brand_type", "quantity_sold")
        ctx_parts.append(gs.to_markdown(index=False))
        rev = group_stats(df, "brand_type", "revenue")
        ctx_parts.append("Doanh thu:")
        ctx_parts.append(rev.to_markdown(index=False))

        # Bổ sung theo danh mục để trả lời các câu hỏi kiểu: 'danh mục nào doanh thu cao nhất?'
        if "category_name" in df.columns:
            # Top danh mục theo doanh thu
            by_cat_rev = (
                df.groupby("category_name", observed=False)["revenue"]
                .sum()
                .sort_values(ascending=False)
                .reset_index(name="revenue_sum")
            )
            if len(by_cat_rev) > 0:
                by_cat_rev["revenue_pct"] = (by_cat_rev["revenue_sum"] / by_cat_rev["revenue_sum"].sum() * 100).round(2)
            ctx_parts.append("Doanh thu theo danh mục (Top 15):")
            ctx_parts.append(by_cat_rev.head(15).to_markdown(index=False))

            # Top danh mục theo lượng bán
            by_cat_qty = (
                df.groupby("category_name", observed=False)["quantity_sold"]
                .sum()
                .sort_values(ascending=False)
                .reset_index(name="qty_sum")
            )
            if len(by_cat_qty) > 0:
                by_cat_qty["qty_pct"] = (by_cat_qty["qty_sum"] / by_cat_qty["qty_sum"].sum() * 100).round(2)
            ctx_parts.append("Lượng bán theo danh mục (Top 15):")
            ctx_parts.append(by_cat_qty.head(15).to_markdown(index=False))

            # Doanh thu theo danh mục × brand_type (để trả lời câu hỏi về cấu trúc từng danh mục)
            ctx_parts.append("Doanh thu theo danh mục × loại thương hiệu (Top 25 dòng):")
            by_cat_bt = (
                df.groupby(["category_name", "brand_type"], observed=False)["revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(25)
                .reset_index(name="revenue_sum")
            )
            ctx_parts.append(by_cat_bt.to_markdown(index=False))

    elif mt_code == "MT2":
        ctx_parts.append("--- Phân khúc Thị trường ---")
        # Tổng lượng bán theo phân khúc × brand_type
        seg = (
            df.groupby(["price_segment", "brand_type"], observed=False)["quantity_sold"]
            .sum()
            .reset_index(name="qty_sum")
        )
        ctx_parts.append("Lượng bán theo Phân khúc giá × Loại thương hiệu:")
        ctx_parts.append(seg.to_markdown(index=False))

        # Tổng lượng bán theo phân khúc (để trả lời 'điểm rơi')
        seg_total = (
            df.groupby("price_segment", observed=False)["quantity_sold"]
            .sum()
            .sort_values(ascending=False)
            .reset_index(name="qty_sum")
        )
        if len(seg_total) > 0:
            seg_total["qty_pct"] = (seg_total["qty_sum"] / seg_total["qty_sum"].sum() * 100).round(2)
        ctx_parts.append("Tổng lượng bán theo Phân khúc giá (xếp hạng):")
        ctx_parts.append(seg_total.to_markdown(index=False))

        # Mật độ sản phẩm: category × price_segment (heatmap)
        if "category_name" in df.columns:
            dens = (
                df.groupby(["category_name", "price_segment"], observed=False)
                .size()
                .reset_index(name="product_count")
            )
            pivot = dens.pivot_table(
                index="category_name",
                columns="price_segment",
                values="product_count",
                fill_value=0,
                observed=False,
            )
            ctx_parts.append("Mật độ sản phẩm: Danh mục × Phân khúc giá (bảng pivot):")
            ctx_parts.append(pivot.to_markdown())

    elif mt_code == "MT3":
        ctx_parts.append("--- Price Premium ---")
        ctx_parts.append(price_premium_stats(df))
        if "category_name" in df.columns:
            med = (
                df.groupby(["category_name", "brand_type"], observed=False)["price"]
                .median()
                .reset_index(name="median_price")
                .sort_values("median_price", ascending=False)
            )
            ctx_parts.append("Giá trung vị theo Danh mục × Loại thương hiệu (xếp hạng):")
            ctx_parts.append(med.to_markdown(index=False))

        # Thêm các phân vị để AI trả lời tốt hơn về 'premium' và outlier
        try:
            q = (
                df.groupby("brand_type", observed=False)["price"]
                .quantile([0.25, 0.5, 0.75])
                .unstack()
                .reset_index()
                .rename(columns={0.25: "p25", 0.5: "median", 0.75: "p75"})
            )
            ctx_parts.append("Phân vị giá theo brand_type (P25/Median/P75):")
            ctx_parts.append(q.to_markdown(index=False))
        except Exception:
            pass

    elif mt_code == "MT4":
        ctx_parts.append("--- Chiến lược Giảm giá ---")
        disc = (
            df.groupby(["brand_type", "discount_flag"], observed=False)
            .size()
            .reset_index(name="count")
        )
        # Thêm % để AI dễ so sánh mức độ chiến tranh giá
        total_by_brand = disc.groupby("brand_type", observed=False)["count"].transform("sum")
        disc["pct"] = (disc["count"] / total_by_brand * 100).round(2)
        ctx_parts.append("Tỷ lệ sản phẩm theo nhãn giảm giá (discount_flag) × brand_type:")
        ctx_parts.append(disc.to_markdown(index=False))

        # Discount rate stats theo brand
        try:
            dr = df.copy()
            dr["discount_pct"] = dr["discount_rate"] * 100
            dr_stats = (
                dr.groupby("brand_type", observed=False)["discount_pct"]
                .agg(["count", "mean", "median", "std", "min", "max"])
                .reset_index()
            )
            ctx_parts.append("Thống kê % giảm giá theo brand_type:")
            ctx_parts.append(dr_stats.to_markdown(index=False))
        except Exception:
            pass

        # Mức giảm giá TB theo danh mục × brand (Top 25 dòng)
        if "category_name" in df.columns:
            avg_disc = (
                df.groupby(["category_name", "brand_type"], observed=False)["discount_rate"]
                .mean()
                .reset_index(name="avg_discount_rate")
            )
            avg_disc["avg_discount_pct"] = (avg_disc["avg_discount_rate"] * 100).round(2)
            avg_disc = avg_disc.sort_values("avg_discount_pct", ascending=False).head(25)
            ctx_parts.append("Giảm giá TB theo Danh mục × brand_type (Top 25):")
            ctx_parts.append(avg_disc[["category_name", "brand_type", "avg_discount_pct"]].to_markdown(index=False))

    elif mt_code == "MT5":
        ctx_parts.append("--- Tiki Trading vs Third-Party ---")
        # Bảng so sánh 3 metrics đúng với chart
        if "channel" in df.columns:
            base = (
                df.groupby("channel", observed=False)
                .agg(
                    product_count=("product_id", "nunique") if "product_id" in df.columns else ("channel", "size"),
                    avg_qty=("quantity_sold", "mean"),
                    median_qty=("quantity_sold", "median"),
                    avg_review=("review_count", "mean"),
                    avg_rating=("rating_average", "mean"),
                )
                .reset_index()
            )
            ctx_parts.append("So sánh theo kênh (product_count, avg/median qty, avg review, avg rating):")
            ctx_parts.append(base.to_markdown(index=False))

            sold_rate = (
                df.assign(is_sold=(df["quantity_sold"] > 0).astype(int))
                .groupby("channel", observed=False)["is_sold"]
                .mean()
                .mul(100)
                .round(2)
                .reset_index(name="sold_product_pct")
            )
            ctx_parts.append("% sản phẩm có đơn (quantity_sold > 0) theo kênh:")
            ctx_parts.append(sold_rate.to_markdown(index=False))

        # Curation: tỷ lệ Tiki Trading/Third-Party theo brand_type
        if "brand_type" in df.columns and "channel" in df.columns:
            cur = (
                df.groupby(["brand_type", "channel"], observed=False)
                .size()
                .reset_index(name="count")
            )
            total_bt = cur.groupby("brand_type", observed=False)["count"].transform("sum")
            cur["pct"] = (cur["count"] / total_bt * 100).round(2)
            ctx_parts.append("Curation: phân bổ kênh theo brand_type (%):")
            ctx_parts.append(cur.to_markdown(index=False))

    elif mt_code == "MT6":
        ctx_parts.append("--- Tỷ lệ Chuyển đổi ---")
        conv = conversion_rate(df, "brand_type")
        ctx_parts.append(conv.to_markdown(index=False))
        conv_cat = conversion_rate(df, "category_name")
        ctx_parts.append(conv_cat.to_markdown(index=False))

        # Ma trận brand_type × channel (đúng với heatmap MT6)
        if "channel" in df.columns:
            total = df.groupby(["brand_type", "channel"], observed=False).size().reset_index(name="total")
            sold = df[df["quantity_sold"] > 0].groupby(["brand_type", "channel"], observed=False).size().reset_index(name="sold")
            merged = total.merge(sold, on=["brand_type", "channel"], how="left").fillna(0)
            merged["conversion_rate"] = (merged["sold"] / merged["total"] * 100).round(2)
            ctx_parts.append("Ma trận chuyển đổi brand_type × channel:")
            ctx_parts.append(merged.to_markdown(index=False))

        # Top/bottom danh mục theo conversion_rate để AI có insight rõ
        if "category_name" in df.columns:
            conv_cat_sorted = conv_cat.sort_values("conversion_rate", ascending=False)
            ctx_parts.append("Top 8 danh mục có conversion_rate cao nhất:")
            ctx_parts.append(conv_cat_sorted.head(8).to_markdown(index=False))
            ctx_parts.append("Bottom 8 danh mục có conversion_rate thấp nhất:")
            ctx_parts.append(conv_cat_sorted.tail(8).to_markdown(index=False))

    elif mt_code == "MT7":
        ctx_parts.append("--- Độ tin cậy Rating ---")
        ss = suspect_rating_stats(df)
        ctx_parts.append(str(ss))
        # So sánh rating TB giữa bình thường và nghi vấn
        if "suspect_label" in df.columns:
            rating_cmp = (
                df.groupby("suspect_label", observed=False)["rating_average"]
                .mean()
                .round(4)
                .reset_index(name="avg_rating")
            )
            ctx_parts.append("Rating trung bình theo nhóm (Bình thường vs Nghi vấn):")
            ctx_parts.append(rating_cmp.to_markdown(index=False))

        # Tỷ trọng nghi vấn theo brand_type
        if "brand_type" in df.columns:
            by_brand = (
                df.groupby("brand_type", observed=False)["is_rating_suspect"]
                .mean()
                .mul(100)
                .round(2)
                .reset_index(name="suspect_pct")
            )
            ctx_parts.append("% sản phẩm nghi vấn theo brand_type:")
            ctx_parts.append(by_brand.to_markdown(index=False))

        # % nghi vấn theo danh mục (đúng với bar ranking MT7)
        if "category_name" in df.columns:
            by_cat = (
                df.groupby("category_name", observed=False)["is_rating_suspect"]
                .mean()
                .mul(100)
                .round(2)
                .reset_index(name="suspect_pct")
                .sort_values("suspect_pct", ascending=False)
            )
            ctx_parts.append("% sản phẩm nghi vấn theo danh mục (xếp hạng):")
            ctx_parts.append(by_cat.to_markdown(index=False))

    elif mt_code == "MT8":
        ctx_parts.append("--- Yếu tố ảnh hưởng Doanh số ---")
        corr_cols = ["price", "rating_average", "review_count", "quantity_sold", "discount_rate"]
        cm = correlation_matrix(df, corr_cols)
        ctx_parts.append(cm.to_markdown())
        try:
            candidates = ["price", "rating_average", "review_count", "discount_rate"]
            model, selected_cols, crit_value = stepwise_ols_regression(
                df,
                "quantity_sold",
                candidates,
                criterion="aic",
                max_steps=30,
            )
            ctx_parts.append("Step-wise OLS (criterion=AIC):")
            ctx_parts.append(f"Biến được chọn: {selected_cols if selected_cols else '[chỉ intercept]'}")
            ctx_parts.append(f"AIC cuối: {crit_value:.4f}")
            ctx_parts.append("OLS Regression Summary:")
            ctx_parts.append(ols_summary_text(model))
        except Exception as e:
            ctx_parts.append(f"OLS Error: {e}")

    return "\n".join(ctx_parts)


def build_context_for_query(df: pd.DataFrame, mt_code: str, user_query: str, base_context: str | None = None) -> str:
    """Context theo MT + bổ sung bảng thống kê theo câu hỏi thực tế (query-aware)."""
    base = base_context if base_context is not None else build_context_for_mt(df, mt_code)
    q = (user_query or "").strip().lower()
    if not q:
        return base

    extra: list[str] = []

    # Nếu user hỏi về giá theo danh mục / ngành hàng (đặc biệt kèm Local/Global)
    if ("giá" in q or "price" in q) and ("danh mục" in q or "ngành" in q or "ngành hàng" in q or "category" in q):
        bt = _brand_type_from_query(q)
        _append_price_by_category(extra, df, brand_type=bt, top_n=12)
        # Nếu có phân khúc giá trong câu hỏi/đang ở MT2 thì thêm breakdown theo segment
        if "phân khúc" in q or "segment" in q or mt_code == "MT2":
            _append_price_segment_by_category(extra, df, brand_type=bt, top_n=20)

    # Nếu user hỏi về doanh thu theo danh mục mà đang ở MT khác
    if ("doanh thu" in q or "revenue" in q) and ("danh mục" in q or "ngành" in q or "category" in q):
        if "category_name" in df.columns and "revenue" in df.columns:
            by_cat = (
                df.groupby("category_name", observed=False)["revenue"]
                .sum()
                .sort_values(ascending=False)
                .head(12)
                .reset_index(name="revenue_sum")
            )
            extra.append("Doanh thu theo danh mục (Top 12):")
            extra.append(by_cat.to_markdown(index=False))

    if not extra:
        return base

    return base + "\n\n--- BỔ SUNG THEO CÂU HỎI (Query-aware) ---\n" + "\n".join(extra)
