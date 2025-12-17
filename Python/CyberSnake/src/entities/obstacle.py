from __future__ import annotations
from dataclasses import dataclass, field
from typing import Set, Tuple

import pygame

from config import CELL_SIZE, GAME_AREA_Y, OBSTACLE_COLOR, OBSTACLE_GLOW

GridPos = Tuple[int, int]

@dataclass
class Obstacles:
    cells: Set[GridPos] = field(default_factory=set)

    def add(self, pos: GridPos) -> None:
        self.cells.add(pos)

    def remove(self, pos: GridPos) -> None:
        self.cells.discard(pos)

    def clear(self) -> None:
        self.cells.clear()

    def draw(self, surface: pygame.Surface) -> None:
        for x, y in self.cells:
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
            for r in range(18, 8, -2):
                alpha = int(60 * (18 - r) / 18)
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*OBSTACLE_GLOW, alpha), (r, r), r)
                surface.blit(s, (center_x - r, center_y - r))
            # simple X marker
            offset = CELL_SIZE // 3
            pygame.draw.line(surface, OBSTACLE_COLOR, (center_x - offset, center_y - offset), (center_x + offset, center_y + offset), 3)
            pygame.draw.line(surface, OBSTACLE_COLOR, (center_x + offset, center_y - offset), (center_x - offset, center_y + offset), 3)

