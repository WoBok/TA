from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
import random
import time
import pygame

from config import CELL_SIZE, GAME_AREA_Y

GridPos = Tuple[int, int]

@dataclass
class SpikeTrap:
    pos: GridPos
    period_ms: int = 1000  # 0.5s hidden + 0.5s shown
    shown_duration_ms: int = 500

    def is_active(self) -> bool:
        t = int(time.time() * 1000) % self.period_ms
        return t >= (self.period_ms - self.shown_duration_ms)

    def draw(self, surface: pygame.Surface):
        x, y = self.pos
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
        active = self.is_active()
        color = (255, 80, 200) if active else (140, 60, 140)
        length = CELL_SIZE // 2 - (0 if active else CELL_SIZE // 3)
        width = 6
        pts = [
            (cx, cy - length),
            (cx - width, cy),
            (cx + width, cy),
        ]
        pygame.draw.polygon(surface, color, pts)

@dataclass
class LavaPool:
    pos: GridPos
    visible_ms: Tuple[int, int] = (3000, 5000)  # visible duration range
    hidden_ms: Tuple[int, int] = (3000, 5000)   # hidden duration range
    _next_toggle: float = 0.0
    _visible: bool = False

    def __post_init__(self):
        self._schedule_next()

    def _schedule_next(self):
        now = time.time()
        if self._visible:
            dur = random.randint(*self.hidden_ms) / 1000.0
        else:
            dur = random.randint(*self.visible_ms) / 1000.0
        self._visible = not self._visible
        self._next_toggle = now + dur

    def update(self):
        if time.time() >= self._next_toggle:
            self._schedule_next()

    def is_active(self) -> bool:
        return self._visible

    def draw(self, surface: pygame.Surface):
        self.update()
        x, y = self.pos
        rect = pygame.Rect(x * CELL_SIZE, GAME_AREA_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        color = (255, 80, 0, 180) if self._visible else (120, 30, 0, 100)
        s = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s, color, s.get_rect(), border_radius=6)
        surface.blit(s, rect)

