from __future__ import annotations
import json
import os
from typing import Any, Dict

DEFAULT_SETTINGS: Dict[str, Any] = {
    "show_fps": False,
    "log_events": False,
}

class SettingsService:
    def __init__(self, path: str = "CyberSnake/settings.json") -> None:
        self.path = path
        self._data: Dict[str, Any] = {}
        self.load()

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
        # Ensure defaults present
        changed = False
        for k, v in DEFAULT_SETTINGS.items():
            if k not in self._data:
                self._data[k] = v
                changed = True
        if changed:
            self.save()

    def save(self) -> None:
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self._data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def get(self, key: str) -> Any:
        return self._data.get(key, DEFAULT_SETTINGS.get(key))

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self.save()

    @property
    def show_fps(self) -> bool:
        return bool(self.get("show_fps"))

    @show_fps.setter
    def show_fps(self, value: bool) -> None:
        self.set("show_fps", bool(value))

    @property
    def log_events(self) -> bool:
        return bool(self.get("log_events"))

    @log_events.setter
    def log_events(self, value: bool) -> None:
        self.set("log_events", bool(value))

