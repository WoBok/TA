from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Any, Optional, List, Tuple
from dataclasses import dataclass

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

@dataclass
class PluginMetadata:
    name: str
    version: str = "1.0.0"
    author: str = "Unknown"
    description: str = ""

class PluginModule(ABC):
    def __init__(self):
        self.metadata = PluginMetadata(name=self.__class__.__name__)
        self.enabled = True
    
    @abstractmethod
    def get_metadata(self) -> PluginMetadata:
        pass
    
    @abstractmethod
    def initialize(self, world: "World", event_bus: "EventBus") -> None:
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        pass
    
    def on_enable(self) -> None:
        pass
    
    def on_disable(self) -> None:
        pass

class FoodPlugin(ABC):
    @abstractmethod
    def get_food_type(self) -> str:
        pass
    
    @abstractmethod
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        pass
    
    @abstractmethod
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        pass
    
    def get_spawn_weight(self) -> float:
        return 1.0
    
    def get_spawn_conditions(self) -> Dict[str, Any]:
        return {}
    
    def can_spawn(self, world: "World", position: Vec2) -> bool:
        return True

class ObstaclePlugin(ABC):
    @abstractmethod
    def get_obstacle_type(self) -> str:
        pass
    
    @abstractmethod
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        pass
    
    @abstractmethod
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        pass
    
    def update_obstacle(self, world: "World", obstacle_entity: "Entity", dt: float) -> None:
        pass
    
    def get_spawn_weight(self) -> float:
        return 1.0
    
    def is_deadly(self) -> bool:
        return True

class EnemyPlugin(ABC):
    @abstractmethod
    def get_enemy_type(self) -> str:
        pass
    
    @abstractmethod
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        pass
    
    @abstractmethod
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        pass
    
    @abstractmethod
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        pass
    
    def is_boss(self) -> bool:
        return False
    
    def get_spawn_weight(self) -> float:
        return 1.0
    
    def get_spawn_conditions(self) -> Dict[str, Any]:
        return {}

class SnakeModifierPlugin(ABC):
    @abstractmethod
    def get_modifier_type(self) -> str:
        pass
    
    @abstractmethod
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        pass
    
    def can_apply(self, world: "World", snake_entity: "Entity") -> bool:
        return True
    
    def get_duration(self) -> float:
        return 0.0
    
    def on_modifier_end(self, world: "World", snake_entity: "Entity") -> None:
        pass
