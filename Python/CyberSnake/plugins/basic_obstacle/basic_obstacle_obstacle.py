from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from src.plugins.plugin_interface import ObstaclePlugin
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    ObstacleComponent,
    CollisionComponent
)
from config import OBSTACLE_COLOR, OBSTACLE_GLOW

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class StaticObstaclePlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        return "static"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = OBSTACLE_COLOR
        render_comp.glow_color = OBSTACLE_GLOW
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "static"
        obstacle_comp.deadly = True
        obstacle_comp.movable = False
        entity.add_component(obstacle_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        entity.add_tag("static_obstacle")
        
        return entity
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        obstacle_comp = obstacle_entity.get_component(ObstacleComponent)
        if obstacle_comp and obstacle_comp.deadly:
            event_bus.publish("game_over", {
                "reason": "Hit obstacle",
                "entity": collider_entity
            })
    
    def is_deadly(self) -> bool:
        return True
