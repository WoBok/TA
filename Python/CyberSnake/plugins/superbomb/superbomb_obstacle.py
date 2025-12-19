from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from src.plugins.plugin_interface import ObstaclePlugin
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    ObstacleComponent,
    CollisionComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class ExplosionDebrisPlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        return "explosion_debris"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (150, 150, 150)
        render_comp.glow_color = (100, 100, 100)
        render_comp.radius = 8
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "explosion_debris"
        obstacle_comp.deadly = False
        obstacle_comp.movable = True
        entity.add_component(obstacle_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        entity.add_tag("explosion_debris")
        
        return entity
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        pass
    
    def is_deadly(self) -> bool:
        return False
