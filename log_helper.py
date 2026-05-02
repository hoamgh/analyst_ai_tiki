"""
log_helper.py — Giao thức ghi vết (Logging Protocol)
Tuân thủ logprompt.md: ghi mọi tương tác vào prompt_logs.csv.
"""
import os
import csv
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "prompt_logs.csv")
HEADERS = ["Timestamp", "Objective", "User_Query", "System_Context", "AI_Response"]


def _ensure_file():
    """Tạo file CSV với header nếu chưa tồn tại."""
    if not os.path.exists(LOG_PATH):
        with open(LOG_PATH, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def log_interaction(objective: str, user_query: str, system_context: str, ai_response: str):
    """
    Ghi một dòng log theo cấu trúc logprompt.md:
      Objective | User_Query | System_Context | AI_Response
    """
    _ensure_file()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, objective, user_query, system_context, ai_response])
