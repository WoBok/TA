from __future__ import annotations

from typing import Protocol, Tuple, List
import pygame

Vec2 = Tuple[int, int]


class AIEnemy(Protocol):
    body: List[Vec2]

    def head(self) -> Vec2: ...

    def update_ai(self, target_foods: List[Vec2]) -> None: ...

    def step(self, grow: bool = False) -> None: ...

    def draw(self, surface: pygame.Surface) -> None: ...
