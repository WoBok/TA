from __future__ import annotations

from typing import Any, Protocol


class GameContext(Protocol):
    score: int
    effects: Any
    obstacles: Any

    def shrink_snake(self, amount: int) -> None: ...
