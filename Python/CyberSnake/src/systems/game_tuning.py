from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from src.managers.settings import SettingsService


@dataclass(frozen=True)
class GameTuning:
    combo_window_ms: int = 2000
    boss_food_threshold: int = 10

    energy_food_spawn_chance: float = 0.3
    traps_min: int = 3
    traps_max: int = 5

    item_spawn_interval_ms: int = 8000
    max_items: int = 2

    ai_spawn_interval_min_ms: int = 10000
    ai_spawn_interval_max_ms: int = 15000
    max_ai_snakes: int = 1

    @staticmethod
    def from_settings(settings: SettingsService) -> GameTuning:
        raw = settings.get("tuning")
        if not isinstance(raw, Mapping):
            return GameTuning()

        def _int(key: str, default: int) -> int:
            v = raw.get(key, default)
            try:
                return int(v)
            except Exception:
                return default

        def _float(key: str, default: float) -> float:
            v = raw.get(key, default)
            try:
                return float(v)
            except Exception:
                return default

        return GameTuning(
            combo_window_ms=_int("combo_window_ms", 2000),
            boss_food_threshold=_int("boss_food_threshold", 10),
            energy_food_spawn_chance=_float("energy_food_spawn_chance", 0.3),
            traps_min=_int("traps_min", 3),
            traps_max=_int("traps_max", 5),
            item_spawn_interval_ms=_int("item_spawn_interval_ms", 8000),
            max_items=_int("max_items", 2),
            ai_spawn_interval_min_ms=_int("ai_spawn_interval_min_ms", 10000),
            ai_spawn_interval_max_ms=_int("ai_spawn_interval_max_ms", 15000),
            max_ai_snakes=_int("max_ai_snakes", 1),
        )
