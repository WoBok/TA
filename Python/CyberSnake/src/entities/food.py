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

        # pulse 0-1-0
        pulse = abs((pygame.time.get_ticks() % 1000) / 500 - 1)

        # glow (pulse)
        glow_radius = int(CELL_SIZE * 0.8 + pulse * 8)
        for r in range(glow_radius, CELL_SIZE // 2, -2):
            alpha = int(60 * (1 - (glow_radius - r) / max(1, glow_radius)))
            s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*FOOD_GLOW, max(0, alpha)), (r, r), r)
            surface.blit(s, (cx - r, cy - r))

        # body
        pygame.draw.circle(surface, FOOD_COLOR, (cx, cy), CELL_SIZE // 2 - 2)
        # highlight
        pygame.draw.circle(surface, (255, 150, 200), (cx - 3, cy - 3), CELL_SIZE // 4)


@dataclass
class EnergyFood:
    pos: GridPos

    def draw(self, surface: pygame.Surface) -> None:
        x, y = self.pos
        cx = x * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2

        # pulse 0-1-0
        pulse = abs((pygame.time.get_ticks() % 1000) / 500 - 1)

        # pulsing glow box
        glow_size = int(pulse * 6)
        for offset in range(6, 0, -1):
            glow_rect = pygame.Rect(
                x * CELL_SIZE - offset - glow_size,
                GAME_AREA_Y + y * CELL_SIZE - offset - glow_size,
                CELL_SIZE + (offset + glow_size) * 2,
                CELL_SIZE + (offset + glow_size) * 2,
            )
            alpha_surf = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            alpha = 40 // offset
            pygame.draw.rect(alpha_surf, (*ENERGY_GLOW, alpha), alpha_surf.get_rect(), border_radius=10)
            surface.blit(alpha_surf, glow_rect)

        # diamond
        pts = [
            (cx, cy - CELL_SIZE // 2 + 2),
            (cx + CELL_SIZE // 2 - 2, cy),
            (cx, cy + CELL_SIZE // 2 - 2),
            (cx - CELL_SIZE // 2 + 2, cy),
        ]
        pygame.draw.polygon(surface, ENERGY_FOOD_COLOR, pts)
        # inner highlight
        inner = [
            (cx, cy - CELL_SIZE // 4),
            (cx + CELL_SIZE // 4, cy),
            (cx, cy + CELL_SIZE // 4),
            (cx - CELL_SIZE // 4, cy),
        ]
        pygame.draw.polygon(surface, (255, 255, 150), inner)

