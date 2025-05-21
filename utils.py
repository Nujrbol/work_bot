# utils.py

import re
import json
import os

DB_FILE = "db.json"

BANNED_WORDS = ["вк", "подпишись", "заработок", "crypto", "bitcoin", "крипта"]

def is_spam(text: str) -> str | None:
    if any(word in text.lower() for word in BANNED_WORDS):
        return "запрещённое слово"
    if text.count("http") > 0 or text.count("t.me") > 0:
        return "ссылки запрещены"
    if sum(map(str.isupper, text)) / len(text) > 0.7:
        return "слишком много заглавных букв"
    return None

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
