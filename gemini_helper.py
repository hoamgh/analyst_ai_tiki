"""
gemini_helper.py — Tầng Thông minh (AI)
Kết nối Gemini API để sinh nhận xét chiến lược.
Tuân thủ pre-analyst.md: chỉ gửi văn bản, không gửi hình ảnh.
"""
import os
import time
import google.generativeai as genai
from typing import List

# ── Cấu hình API ────────────────────────────────────────────────────
_API_KEY = None
_MODELS = [
    # NOTE: Google đổi tên model theo thời gian; đây chỉ là danh sách ưu tiên ban đầu.
    # Khi gặp lỗi 404/unsupported, code sẽ tự ListModels để chọn model hợp lệ.
    "gemini-2.0-flash",
    "gemini-1.5-flash",
]
MAX_RETRIES = 3

_DISCOVERED_MODELS: List[str] | None = None


def _discover_models() -> List[str]:
    """Tự dò model khả dụng và có hỗ trợ generateContent (tránh hard-code bị 404)."""
    global _DISCOVERED_MODELS
    if _DISCOVERED_MODELS is not None:
        return _DISCOVERED_MODELS

    discovered: List[str] = []
    try:
        for m in genai.list_models():
            name = getattr(m, "name", None)
            methods = getattr(m, "supported_generation_methods", None) or []
            if name and ("generateContent" in methods):
                discovered.append(str(name))  # thường có dạng: models/xxxxx
    except Exception:
        _DISCOVERED_MODELS = []
        return _DISCOVERED_MODELS

    def _score(model_name: str) -> tuple:
        s = model_name.lower()
        # Ưu tiên flash (rẻ/nhanh) trước, rồi pro.
        return (
            0 if "flash" in s else 1,
            0 if "pro" in s else 1,
            len(s),
        )

    discovered = sorted(set(discovered), key=_score)
    _DISCOVERED_MODELS = discovered
    return discovered

def _load_api_key() -> str:
    global _API_KEY
    if _API_KEY:
        return _API_KEY
    env_path = os.path.join(os.path.dirname(__file__), "api.env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            _API_KEY = f.read().strip()
    else:
        _API_KEY = os.getenv("GEMINI_API_KEY", "")
    return _API_KEY


def ask_gemini(system_context: str, user_query: str, mt_code: str) -> str:
    """
    Gửi câu hỏi tới Gemini API với ngữ cảnh thống kê.
    Có retry logic + fallback model khi bị rate-limit.
    """
    api_key = _load_api_key()
    if not api_key:
        return "⚠️ Chưa cấu hình API Key Gemini. Vui lòng đặt key vào file api.env."

    genai.configure(api_key=api_key)

    prompt = f"""Bạn là chuyên gia phân tích chiến lược thương mại điện tử Tiki.
Vai trò: Phân tích dữ liệu thực tế từ pipeline crawl Tiki Electronics 2026.

[QUY TẮC BẮT BUỘC]
1. CHỈ trả lời dựa trên dữ liệu thống kê bên dưới. KHÔNG sử dụng kiến thức bên ngoài.
2. Mọi nhận xét phải kèm số liệu cụ thể để minh chứng.
3. Nếu dữ liệu không đủ để trả lời, hãy từ chối và nêu rõ lý do.
4. Trả lời bằng tiếng Việt, ngắn gọn, súc tích.
5. Cấu trúc: Xu hướng chính → Điểm bất thường → Khuyến nghị hành động.

{system_context}

[CÂU HỎI NGƯỜI DÙNG — {mt_code}]
{user_query}

[YÊU CẦU]
Hãy phân tích và trả lời. Bắt buộc sử dụng số liệu ở trên để minh chứng.
Định dạng trả lời bằng Markdown với emoji phù hợp."""

    # Thử từng model với retry (hard-code trước, nếu lỗi 404/unsupported thì tự dò ListModels)
    models_to_try: List[str] = list(_MODELS)
    discovered_used = False

    for _ in range(2):
        for model_name in models_to_try:
            for attempt in range(MAX_RETRIES):
                try:
                    model = genai.GenerativeModel(model_name)
                    response = model.generate_content(prompt)
                    return response.text
                except Exception as e:
                    err = str(e)
                    err_lower = err.lower()

                    # Rate limit / quota → retry
                    if "429" in err or "quota" in err_lower:
                        wait = min(2 ** attempt * 5, 30)  # 5s, 10s, 20s
                        time.sleep(wait)
                        continue

                    # Model không tồn tại/không hỗ trợ generateContent → chuyển sang autodiscover
                    if ("404" in err_lower) or ("not found" in err_lower) or ("not supported" in err_lower):
                        break  # dừng retry model này

                    # Lỗi khác → trả về luôn
                    return f"❌ Lỗi Gemini API: {err}"

        if discovered_used:
            break
        # Sau vòng hard-code mà không thành công → autodiscover model hợp lệ
        discovered = _discover_models()
        if not discovered:
            break
        models_to_try = discovered
        discovered_used = True

    return ("⚠️ **Đã hết quota Gemini API miễn phí trong ngày.**\n\n"
            "💡 **Cách khắc phục:**\n"
            "1. Tạo API Key mới từ project mới tại [aistudio.google.com/apikey](https://aistudio.google.com/apikey)\n"
            "2. Dán key mới vào file `api.env` rồi refresh trang\n"
            "3. Hoặc chờ đến ngày mai để quota được reset")
