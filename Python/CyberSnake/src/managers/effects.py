from __future__ import annotations
import time
from dataclasses import dataclass
from typing import Optional, Tuple, TYPE_CHECKING, List

from config import CELL_SIZE, GAME_AREA_Y
from src.entities.particle import ParticleSystem
from src.managers.input_manager import InputManager

if TYPE_CHECKING:
    from src.entities.food import Food, EnergyFood

@dataclass
class MagnetEffect:
    active: bool = False
    radius_cells: int = 0
    end_time: float = 0.0

class EffectsManager:
    """Centralized gameplay effects manager."""
    def __init__(self, particles: ParticleSystem, input_mgr: Optional[InputManager]):
        self.particles = particles
        self.input_mgr = input_mgr
        self.magnet = MagnetEffect()
        self.inverted_until: float = 0.0
        self.rainbow_trail_until: float = 0.0

    def enable_magnet(self, radius_cells: int, duration_ms: int):
        self.magnet.active = True
        self.magnet.radius_cells = radius_cells
        self.magnet.end_time = time.time() + duration_ms / 1000.0

    def update_magnet(self):
        if self.magnet.active and time.time() >= self.magnet.end_time:
            self.magnet.active = False

    def apply_magnet_pull(self, head_pos: Tuple[int, int], foods: List[Food | EnergyFood | None]):
        if not self.magnet.active: return
        hx, hy = head_pos
        radius_sq = self.magnet.radius_cells ** 2
        for food_item in foods:
            if food_item is None: continue
            fx, fy = food_item.pos
            if (hx - fx)**2 + (hy - fy)**2 <= radius_sq:
                new_fx = fx + (1 if hx > fx else -1 if hx < fx else 0)
                new_fy = fy + (1 if hy > fy else -1 if hy < fy else 0)
                food_item.pos = (new_fx, new_fy)
                self.particles.emit(new_fx * CELL_SIZE + CELL_SIZE // 2, GAME_AREA_Y + new_fy * CELL_SIZE + CELL_SIZE // 2, (255, 255, 100), count=2)

    def trigger_bomb_explosion(self, center_pos: Tuple[int, int]):
        px = center_pos[0] * CELL_SIZE + CELL_SIZE // 2
        py = GAME_AREA_Y + center_pos[1] * CELL_SIZE + CELL_SIZE // 2
        self.particles.emit(px, py, (255, 100, 0), count=50)

    def trigger_shrink_effect(self, positions: List[Tuple[int, int]]):
        """Spawns 'bubble pop' particles at given tail positions."""
        for pos in positions:
            px = pos[0] * CELL_SIZE + CELL_SIZE // 2
            py = GAME_AREA_Y + pos[1] * CELL_SIZE + CELL_SIZE // 2
            self.particles.emit(px, py, (100, 200, 255), count=15)

    def enable_inverted_controls(self, duration_ms: int):
        now = time.time()
        duration_sec = duration_ms / 1000.0
        self.inverted_until = now + duration_sec
        self.rainbow_trail_until = now + duration_sec
        if self.input_mgr: self.input_mgr.set_inverted(True)

    def update_inverted(self):
        now = time.time()
        if self.input_mgr and self.input_mgr.inverted and now >= self.inverted_until:
            self.input_mgr.set_inverted(False)
        if now >= self.rainbow_trail_until:
            self.rainbow_trail_until = 0.0

    @property
    def is_rainbow_trail_active(self) -> bool:
        return time.time() < self.rainbow_trail_until

    def update(self, head_pos: Tuple[int, int], foods: List[Food | EnergyFood | None]):
        self.update_magnet()
        self.update_inverted()
        self.apply_magnet_pull(head_pos, foods)
