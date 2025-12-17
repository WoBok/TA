from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, Optional, TYPE_CHECKING

import pygame

from typing import Tuple, Optional, TYPE_CHECKING, List

if TYPE_CHECKING:
    from src.scenes.game_scene import GameScene

# Item system stubs to support future gameplay expansion

@dataclass
class Item:
    pos: Tuple[int, int]
    color: Tuple[int, int, int] = (255, 255, 255)
    duration_ms: int = 0  # 0 means instant effect

    def apply(self, game: "GameScene") -> None:
        """Apply the effect to the game. To be implemented in subclasses."""
        raise NotImplementedError

    def draw(self, surface: pygame.Surface, cell_size: int, origin_y: int):
        # Default: draw a glowing circle at grid position
        cx = self.pos[0] * cell_size + cell_size // 2
        cy = origin_y + self.pos[1] * cell_size + cell_size // 2
        for r in range(int(cell_size * 0.8), cell_size // 2, -2):
            alpha = int(50 * (1 - (r - cell_size // 2) / (cell_size // 2)))
            s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, max(0, alpha)), (r, r), r)
            surface.blit(s, (cx - r, cy - r))
        pygame.draw.circle(surface, self.color, (cx, cy), cell_size // 2 - 2)


@dataclass
class Magnet(Item):
    color: Tuple[int, int, int] = (255, 255, 0)  # Yellow
    duration_ms: int = 5000
    radius_cells: int = 5

    def apply(self, game: "GameScene"):
        game.effects.enable_magnet(self.radius_cells, self.duration_ms)


@dataclass
class Bomb(Item):
    color: Tuple[int, int, int] = (40, 40, 40)  # Dark Grey/Black

    def apply(self, game: "GameScene"):
        game.obstacles.clear()
        game.effects.trigger_bomb_explosion(self.pos)


@dataclass
class Scissors(Item):
    color: Tuple[int, int, int] = (0, 255, 127) # Green
    reduce_len: int = 4

    def apply(self, game: "GameScene"):
        game.shrink_snake(self.reduce_len)


@dataclass
class RottenApple(Item):
    color: Tuple[int, int, int] = (139, 0, 255) # Purple
    duration_ms: int = 5000

    def apply(self, game: "GameScene"):
        game.effects.enable_inverted_controls(self.duration_ms)

    color: Tuple[int, int, int] = (40, 40, 40)  # Dark Grey/Black

    def apply(self, game: "GameScene"):
        game.obstacles.clear()
        game.effects.trigger_bomb_explosion(self.pos)
