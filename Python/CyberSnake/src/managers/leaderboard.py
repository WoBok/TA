from __future__ import annotations
import json
import os
from typing import List, Dict

from config import LEADERBOARD_FILE, MAX_LEADERBOARD_ENTRIES

Entry = Dict[str, int | str]

def load_leaderboard() -> List[Entry]:
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []

def save_leaderboard(entries: List[Entry]) -> None:
    try:
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def is_high_score(entries: List[Entry], score: int) -> bool:
    if len(entries) < MAX_LEADERBOARD_ENTRIES:
        return True
    return score > int(entries[-1]["score"])  # type: ignore[index]

def add_entry(entries: List[Entry], name: str, score: int) -> List[Entry]:
    entries.append({"name": name, "score": score})
    entries.sort(key=lambda e: int(e["score"]), reverse=True)
    return entries[:MAX_LEADERBOARD_ENTRIES]

