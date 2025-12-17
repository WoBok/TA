from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple
import pygame

from config import CELL_SIZE, GAME_AREA_Y

GridPos = Tuple[int, int]

@dataclass
class PortalPair:
    orange: GridPos
    blue: GridPos

    def teleport(self, pos: GridPos) -> GridPos:
        if pos == self.orange:
            return self.blue
        if pos == self.blue:
            return self.orange
        return pos

    def draw(self, surface: pygame.Surface):
        for pos, color in [(self.orange, (255,140,0)), (self.blue, (0,160,255))]:
            cx = pos[0] * CELL_SIZE + CELL_SIZE // 2
            cy = GAME_AREA_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2
            for r in range(CELL_SIZE // 2, 6, -3):
                s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*color, 120), (r, r), r, width=3)
                surface.blit(s, (cx - r, cy - r))

