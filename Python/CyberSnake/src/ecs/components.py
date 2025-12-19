from __future__ import annotations
from dataclasses import dataclass, field
from typing import Tuple, List, Optional, Callable, Any
import pygame

from .component import Component

Vec2 = Tuple[int, int]
Color = Tuple[int, int, int]

@dataclass
class PositionComponent(Component):
    x: int = 0
    y: int = 0
    
    @property
    def pos(self) -> Vec2:
        return (self.x, self.y)
    
    @pos.setter
    def pos(self, value: Vec2):
        self.x, self.y = value

@dataclass
class VelocityComponent(Component):
    dx: int = 0
    dy: int = 0
    
    @property
    def direction(self) -> Vec2:
        return (self.dx, self.dy)
    
    @direction.setter
    def direction(self, value: Vec2):
        self.dx, self.dy = value

@dataclass
class BodyComponent(Component):
    segments: List[Vec2] = field(default_factory=list)
    
    def head(self) -> Vec2:
        return self.segments[0] if self.segments else (0, 0)
    
    def tail(self) -> Vec2:
        return self.segments[-1] if self.segments else (0, 0)

@dataclass
class RenderComponent(Component):
    color: Color = (255, 255, 255)
    glow_color: Optional[Color] = None
    radius: int = 10
    shape: str = "circle"
    visible: bool = True
    alpha: int = 255
    layer: int = 0

@dataclass
class CollisionComponent(Component):
    collidable: bool = True
    collision_layer: str = "default"
    collision_mask: List[str] = field(default_factory=lambda: ["default"])

@dataclass
class HealthComponent(Component):
    current: int = 1
    maximum: int = 1
    invulnerable: bool = False

@dataclass
class FoodComponent(Component):
    food_type: str = "normal"
    score_value: int = 1
    growth_amount: int = 1
    energy_value: int = 0
    effects: List[str] = field(default_factory=list)

@dataclass
class ObstacleComponent(Component):
    obstacle_type: str = "static"
    deadly: bool = True
    movable: bool = False

@dataclass
class EnemyComponent(Component):
    enemy_type: str = "normal"
    ai_behavior: str = "chase"
    damage: int = 1
    is_boss: bool = False

@dataclass
class SnakeComponent(Component):
    is_player: bool = True
    ghost_mode: bool = False
    ghost_end_time: int = 0
    next_direction: Vec2 = (1, 0)
    glow_effect_active: bool = False
    glow_effect_start: int = 0
    glow_effect_color: Optional[Color] = None
    glow_effect_duration: int = 500

@dataclass
class TimerComponent(Component):
    duration: float = 0.0
    elapsed: float = 0.0
    repeat: bool = False
    callback: Optional[Callable] = None
    
    def is_finished(self) -> bool:
        return self.elapsed >= self.duration

@dataclass
class EffectComponent(Component):
    effect_type: str = "none"
    duration: float = 0.0
    elapsed: float = 0.0
    intensity: float = 1.0
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SpawnComponent(Component):
    spawn_interval: float = 5.0
    last_spawn_time: float = 0.0
    max_spawns: int = -1
    spawn_count: int = 0
    spawn_type: str = "food"

@dataclass
class AIComponent(Component):
    behavior: str = "wander"
    target_entity_id: Optional[str] = None
    update_interval: float = 0.1
    last_update: float = 0.0
    state: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PortalComponent(Component):
    linked_portal_id: Optional[str] = None
    portal_type: str = "orange"
    cooldown: float = 0.5
    last_use_time: float = 0.0

@dataclass
class TrapComponent(Component):
    trap_type: str = "spike"
    damage: int = 1
    active: bool = True
    trigger_delay: float = 0.0

@dataclass
class ItemComponent(Component):
    item_type: str = "speed_boost"
    duration: float = 5.0
    pickup_effect: Optional[Callable] = None

@dataclass
class ParticleComponent(Component):
    lifetime: float = 1.0
    age: float = 0.0
    velocity: Vec2 = (0, 0)
    acceleration: Vec2 = (0, 0)
    fade_out: bool = True
