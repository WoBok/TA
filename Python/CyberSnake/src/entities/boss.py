from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
import time
import pygame
import random

from config import CELL_SIZE, GAME_AREA_Y, GRID_WIDTH, GRID_HEIGHT

Vec2 = Tuple[int, int]

@dataclass
class Bullet:
    pos: Tuple[float, float]
    velocity: Tuple[float, float]
    size: int = 5

    def update(self):
        self.pos = (self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1])

    def is_offscreen(self) -> bool:
        x, y = self.pos
        return not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT)

    def get_grid_pos(self) -> Vec2:
        return (int(self.pos[0]), int(self.pos[1]))

    def draw(self, surface: pygame.Surface):
        cx = self.pos[0] * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + self.pos[1] * CELL_SIZE + CELL_SIZE // 2
        pygame.draw.circle(surface, (255, 100, 100), (cx, cy), self.size)

@dataclass
class Boss:
    pos: Vec2  # Top-left corner of the 3x3 grid
    health: int = 1
    shield_duration: int = 5000
    shield_end_time: float = field(default_factory=lambda: time.time() * 1000 + 5000)
    last_shot_time: float = 0
    shot_interval: int = 1000 # Shoots every 1 second
    bullets: List[Bullet] = field(default_factory=list)

    @property
    def is_shield_active(self) -> bool:
        return time.time() * 1000 < self.shield_end_time

    def get_body_cells(self) -> List[Vec2]:
        cells = []
        for r in range(3):
            for c in range(3):
                cells.append((self.pos[0] + c, self.pos[1] + r))
        return cells

    def update(self, player_head: Vec2):
        now = time.time() * 1000
        if not self.is_shield_active and now - self.last_shot_time > self.shot_interval:
            self.shoot(player_head)
            self.last_shot_time = now
        
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_offscreen():
                self.bullets.remove(bullet)

    def shoot(self, target_pos: Vec2):
        start_pos = (self.pos[0] + 1.5, self.pos[1] + 1.5)
        dx, dy = target_pos[0] - start_pos[0], target_pos[1] - start_pos[1]
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            speed = 0.1 # Grid cells per frame
            velocity = (dx / dist * speed, dy / dist * speed)
            self.bullets.append(Bullet(pos=start_pos, velocity=velocity))

    def draw(self, surface: pygame.Surface):
        # Draw body
        for cell in self.get_body_cells():
            rect = pygame.Rect(cell[0] * CELL_SIZE, GAME_AREA_Y + cell[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, (150, 50, 150), rect)

        # Draw shield
        if self.is_shield_active:
            shield_alpha = 100 * ((self.shield_end_time - time.time() * 1000) / self.shield_duration)
            shield_rect = pygame.Rect(self.pos[0] * CELL_SIZE, GAME_AREA_Y + self.pos[1] * CELL_SIZE, CELL_SIZE * 3, CELL_SIZE * 3).inflate(10, 10)
            s = pygame.Surface(shield_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(s, (100, 100, 255, shield_alpha), s.get_rect(), border_radius=10)
            surface.blit(s, shield_rect.topleft)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(surface)

