from __future__ import annotations
from dataclasses import dataclass
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

        # 刷光进度
        glow_progress = -1.0
        if self.glow_effect_active and self.glow_effect_color is not None:
            elapsed = pygame.time.get_ticks() - self.glow_effect_start
            if elapsed < self.glow_effect_duration:
                glow_progress = elapsed / self.glow_effect_duration
            else:
                self.glow_effect_active = False

        snake_len = len(self.body)

        for i, (x, y) in enumerate(self.body):
            center_x = x * CELL_SIZE + CELL_SIZE // 2
            center_y = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
            
            is_head = (i == 0)
            radius = CELL_SIZE // 2 - 1 if is_head else int(CELL_SIZE * 0.42)
            base_color = SNAKE_HEAD_COLOR if is_head else SNAKE_COLOR
            glow_color = SNAKE_HEAD_COLOR if is_head else SNAKE_GLOW

            # 渐变到尾部稍暗
            if snake_len > 1:
                factor = i / max(1, snake_len - 1)
                base_color = tuple(int(base_color[c] * (1 - factor * 0.3)) for c in range(3))

            # 刷光颜色混合
            is_glowing = False
            if glow_progress >= 0 and snake_len > 0 and self.glow_effect_color is not None:
                glow_pos = glow_progress * snake_len
                glow_width = 3
                if abs(i - glow_pos) < glow_width:
                    is_glowing = True
                    dist_factor = 1.0 - abs(i - glow_pos) / glow_width
                    blend = dist_factor * 0.9
                    base_color = tuple(
                        min(255, int((base_color[c] * (1 - blend) + self.glow_effect_color[c] * blend) * 1.3))
                        for c in range(3)
                    )
                    glow_color = tuple(min(255, int(self.glow_effect_color[c] * 1.2)) for c in range(3))

            if rainbow_effect and not is_head:
                hue = (pygame.time.get_ticks() + i * 35) % 360
                c = pygame.Color(0)
                c.hsla = (hue, 100, 50, now_alpha)
                base_color = (c.r, c.g, c.b)
                glow_color = base_color

            # 发光层
            glow_intensity = 6 if is_glowing else 4
            for r in range(radius + glow_intensity, radius, -1):
                alpha_glow = int((30 if is_glowing else 20) * (1 - (r - radius) / glow_intensity))
                s = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, (*glow_color, alpha_glow), (r, r), r)
                surface.blit(s, (center_x - r, center_y - r))

            # 主体圆球
            ball = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(ball, (*base_color, now_alpha), (radius, radius), radius)

            # 身体高光
            highlight_radius = int(radius * 0.6)
            hx_off = int(radius * 0.3)
            hy_off = int(radius * 0.3)
            highlight_color = tuple(min(255, c + 80) for c in base_color)
            hl_alpha = int(now_alpha * 0.8) if now_alpha < 255 else 200
            pygame.draw.circle(ball, (*highlight_color, hl_alpha), (radius - hx_off, radius - hy_off), highlight_radius)

            # 顶部小高光点
            small_r = int(radius * 0.3)
            sx_off = int(radius * 0.4)
            sy_off = int(radius * 0.4)
            pygame.draw.circle(ball, (255, 255, 255, min(now_alpha, 180)), (radius - sx_off, radius - sy_off), small_r)

            surface.blit(ball, (center_x - radius, center_y - radius))

            # 头部眼睛
            if is_head:
                dx, dy = self.direction
                eye_size = max(2, radius // 4)
                forward = radius // 2
                side = radius // 3
                if dx == 1:
                    e1 = (center_x + forward, center_y - side)
                    e2 = (center_x + forward, center_y + side)
                elif dx == -1:
                    e1 = (center_x - forward, center_y - side)
                    e2 = (center_x - forward, center_y + side)
                elif dy == -1:
                    e1 = (center_x - side, center_y - forward)
                    e2 = (center_x + side, center_y - forward)
                else:
                    e1 = (center_x - side, center_y + forward)
                    e2 = (center_x + side, center_y + forward)
                # 眼睛发光
                for rr in range(eye_size + 2, eye_size, -1):
                    a = int(60 * (1 - (rr - eye_size) / 2))
                    s = pygame.Surface((rr * 2, rr * 2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 255, 255, a), (rr, rr), rr)
                    surface.blit(s, (e1[0] - rr, e1[1] - rr))
                    surface.blit(s, (e2[0] - rr, e2[1] - rr))
                # 眼白
                pygame.draw.circle(surface, (255, 255, 255), e1, eye_size)
                pygame.draw.circle(surface, (255, 255, 255), e2, eye_size)
                # 瞳孔
                pupil = max(1, eye_size // 2)
                pygame.draw.circle(surface, (0, 0, 0), e1, pupil)
                pygame.draw.circle(surface, (0, 0, 0), e2, pupil)
