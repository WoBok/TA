from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple
import random
import time
import pygame

from config import CELL_SIZE, GAME_AREA_Y, GRID_WIDTH, GRID_HEIGHT

Vec2 = Tuple[int, int]

@dataclass
class AISnake:
    body: List[Vec2]
    direction: Vec2 = (1, 0)
    color: Tuple[int, int, int] = (80, 200, 120)

    def head(self) -> Vec2:
        return self.body[0]

    def update_ai(self, target_foods: List[Vec2]):
        """Simple greedy AI that moves towards the nearest food."""
        if not target_foods:
            # Wander randomly if no food
            if random.random() < 0.1:
                self.direction = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
            return
        
        hx, hy = self.head()
        target = min(target_foods, key=lambda p: abs(p[0]-hx) + abs(p[1]-hy))
        
        dx, dy = target[0] - hx, target[1] - hy

        # Prefer horizontal movement, then vertical to avoid getting stuck in loops
        if dx != 0 and (self.direction[0] != -dx or self.direction[1] != 0):
            self.direction = (dx // abs(dx), 0)
        elif dy != 0 and (self.direction[1] != -dy or self.direction[0] != 0):
            self.direction = (0, dy // abs(dy))

    def step(self, grow: bool = False):
        hx, hy = self.head()
        dx, dy = self.direction
        new_head = ((hx + dx) % GRID_WIDTH, (hy + dy) % GRID_HEIGHT) # AI snakes can wrap around walls
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def draw(self, surface: pygame.Surface) -> None:
        for i, (x, y) in enumerate(self.body):
            cx = x * CELL_SIZE + CELL_SIZE // 2
            cy = GAME_AREA_Y + y * CELL_SIZE + CELL_SIZE // 2
            radius = CELL_SIZE // 2 - 2 if i == 0 else int(CELL_SIZE * 0.4)
            pygame.draw.circle(surface, self.color, (cx, cy), radius)

@dataclass
class GhostHunter:
    pos: Vec2
    speed: float = 0.02  # Slow, steady movement
    visible: bool = True
    next_toggle_time: float = 0.0
    color: Tuple[int, int, int] = (255, 50, 50)

    def __post_init__(self):
        self.schedule_next_toggle()

    def schedule_next_toggle(self):
        duration = random.uniform(4, 7) if self.visible else random.uniform(4, 8)
        self.next_toggle_time = time.time() + duration

    def update(self, target_head: Vec2):
        if time.time() > self.next_toggle_time:
            self.visible = not self.visible
            self.schedule_next_toggle()
            if self.visible:
                # Respawn at a random edge
                edge = random.choice(['top', 'bottom', 'left', 'right'])
                if edge == 'top': self.pos = (random.randint(0, GRID_WIDTH-1), -1)
                elif edge == 'bottom': self.pos = (random.randint(0, GRID_WIDTH-1), GRID_HEIGHT)
                elif edge == 'left': self.pos = (-1, random.randint(0, GRID_HEIGHT-1))
                else: self.pos = (GRID_WIDTH, random.randint(0, GRID_HEIGHT-1))

        if not self.visible: return

        # Move towards the player's head
        tx, ty = target_head
        px, py = self.pos
        dx, dy = tx - px, ty - py
        dist = (dx**2 + dy**2)**0.5
        if dist > 0:
            self.pos = (px + self.speed * dx / dist, py + self.speed * dy / dist)

    def get_grid_pos(self) -> Vec2:
        return (int(self.pos[0]), int(self.pos[1]))

    def draw(self, surface: pygame.Surface):
        if not self.visible: return
        
        alpha = 100 + 50 * (time.time() * 3 % 1) # Pulsing alpha
        cx = self.pos[0] * CELL_SIZE + CELL_SIZE // 2
        cy = GAME_AREA_Y + self.pos[1] * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2

        s = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color, alpha), (radius, radius), radius)
        surface.blit(s, (cx - radius, cy - radius))
