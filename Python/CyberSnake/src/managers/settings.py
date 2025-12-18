from __future__ import annotations
import json
import os
from typing import Any, Dict

DEFAULT_SETTINGS: Dict[str, Any] = {
    "show_fps": False,
    "log_events": False,
    "debug_exceptions": False,
    "tuning": {},
}

class SettingsService:
    def __init__(self, path: str = "CyberSnake/settings.json") -> None:
        self.path = path
        self._data: Dict[str, Any] = {}
        self.load()

    def _maybe_print_exception(self) -> None:
        try:
            if self.debug_exceptions:
                import traceback

                traceback.print_exc()
        except Exception:
            pass

    def load(self) -> None:
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as f:
                    self._data = json.load(f)
            except Exception:
                self._data = {}
                self._maybe_print_exception()
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
            self._maybe_print_exception()

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

    @property
    def debug_exceptions(self) -> bool:
        return bool(self.get("debug_exceptions"))

    @debug_exceptions.setter
    def debug_exceptions(self, value: bool) -> None:
        self.set("debug_exceptions", bool(value))
