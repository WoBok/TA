from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

import pygame

from config import CELL_SIZE, GAME_AREA_Y, FOOD_COLOR, FOOD_GLOW, ENERGY_FOOD_COLOR, ENERGY_GLOW

GridPos = Tuple[int, int]

@dataclass
class Food:
    pos: GridPos

    def draw(self, surface: pygame.Surface) -> None:
        x, y = self.pos
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2

        # glow
        for r in range(int(CELL_SIZE * 0.8), CELL_SIZE // 2, -2):
            alpha = int(40 * (1 - (r - CELL_SIZE // 2) / (CELL_SIZE // 2)))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*FOOD_GLOW, max(0, alpha)), (r, r), r)
            surface.blit(s, (cx - r, cy - r))
        pygame.draw.circle(surface, FOOD_COLOR, (cx, cy), CELL_SIZE // 2 - 2)


@dataclass
class EnergyFood:
    pos: GridPos

    def draw(self, surface: pygame.Surface) -> None:
        x, y = self.pos
        rect = pygame.Rect(x * CELL_SIZE, GAME_AREA_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        # glow box
        for grow in range(6, 0, -1):
            glow_rect = rect.inflate(grow * 2, grow * 2)
            alpha_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            alpha = 40 // max(1, grow)
            pygame.draw.rect(alpha_surf, (*ENERGY_GLOW, alpha), alpha_surf.get_rect(), border_radius=10)
            surface.blit(alpha_surf, glow_rect)
        # diamond
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
        pts = [
            (cx, cy - CELL_SIZE // 2 + 2),
            (cx + CELL_SIZE // 2 - 2, cy),
            (cx, cy + CELL_SIZE // 2 - 2),
            (cx - CELL_SIZE // 2 - 2 + 4, cy),
        ]
        pygame.draw.polygon(surface, ENERGY_FOOD_COLOR, pts)

