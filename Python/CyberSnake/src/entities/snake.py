from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

import pygame

from config import CELL_SIZE, GAME_AREA_Y, SNAKE_COLOR, SNAKE_HEAD_COLOR, SNAKE_GLOW

Vec2 = Tuple[int, int]

@dataclass
class Snake:
    body: List[Vec2]
    direction: Vec2 = (1, 0)
    next_direction: Vec2 = (1, 0)

    # visual state
    glow_effect_active: bool = False
    glow_effect_start: int = 0
    glow_effect_color: Tuple[int, int, int] | None = None
    glow_effect_duration: int = 500

    def head(self) -> Vec2:
        # Safety guard to avoid crashes if body becomes empty unexpectedly
        return self.body[0] if self.body else (0, 0)

    def set_direction(self, new_dir: Vec2):
        if (self.direction[0] + new_dir[0], self.direction[1] + new_dir[1]) != (0, 0):
            self.next_direction = new_dir

    def step(self, grow: bool = False):
        self.direction = self.next_direction
        hx, hy = self.body[0]
        dx, dy = self.direction
        nh = (hx + dx, hy + dy)
        self.body.insert(0, nh)
        if not grow:
            self.body.pop()

    def trigger_glow(self, color: Tuple[int, int, int], now_ms: int):
        self.glow_effect_active = True
        self.glow_effect_start = now_ms
        self.glow_effect_color = color

    def draw(self, surface: pygame.Surface, ghost_alpha: int | None = None, rainbow_effect: bool = False):
        now_alpha = 255 if ghost_alpha is None else ghost_alpha

        for i, (x, y) in enumerate(self.body):
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
            
            is_head = (i == 0)
            radius = CELL_SIZE // 2 - 1 if is_head else int(CELL_SIZE * 0.42)
            base_color = SNAKE_HEAD_COLOR if is_head else SNAKE_COLOR
            glow_color = SNAKE_HEAD_COLOR if is_head else SNAKE_GLOW

            if rainbow_effect and not is_head:
                hue = (pygame.time.get_ticks() + i * 35) % 360
                c = pygame.Color(0)
                c.hsla = (hue, 100, 50, now_alpha)
                base_color = (c.r, c.g, c.b)
                glow_color = base_color

            # glow layer
            for r in range(radius + 4, radius, -1):
                alpha_glow = int(20 * (1 - (r - radius) / 4))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*glow_color, alpha_glow), (r, r), r)
                surface.blit(s, (center_x - r, center_y - r))

            # body
            ball = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ball, (*base_color, now_alpha), (radius, radius), radius)
            surface.blit(ball, (center_x - radius, center_y - radius))
