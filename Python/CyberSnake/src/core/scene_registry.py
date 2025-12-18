from __future__ import annotations

from typing import Dict, Type

from src.core.scene import Scene


class SceneRegistry:
    def __init__(self) -> None:
        self._by_key: Dict[str, Type[Scene]] = {}

    def register(self, key: str, scene_cls: Type[Scene]) -> None:
        self._by_key[key] = scene_cls

    def get(self, key: str) -> Type[Scene]:
        return self._by_key[key]
