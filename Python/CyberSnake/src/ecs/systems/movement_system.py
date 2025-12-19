from __future__ import annotations
from typing import TYPE_CHECKING

from src.ecs.system import System
from src.ecs.components import (
    PositionComponent,
    VelocityComponent,
    BodyComponent,
    SnakeComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World

class MovementSystem(System):
    def __init__(self, world: "World", grid_width: int, grid_height: int):
        super().__init__(world)
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.priority = 10
    
    def update(self, dt: float):
        snake_entities = self.get_entities_with_components(SnakeComponent, BodyComponent, VelocityComponent)
        
        for entity in snake_entities:
            snake_comp = entity.get_component(SnakeComponent)
            body_comp = entity.get_component(BodyComponent)
            vel_comp = entity.get_component(VelocityComponent)
            
            if not snake_comp or not body_comp or not vel_comp:
                continue
            
            vel_comp.direction = snake_comp.next_direction
            
            if not body_comp.segments:
                continue
            
            hx, hy = body_comp.head()
            dx, dy = vel_comp.direction
            new_head = (hx + dx, hy + dy)
            
            if snake_comp.is_player:
                new_head = (new_head[0] % self.grid_width, new_head[1] % self.grid_height)
            
            body_comp.segments.insert(0, new_head)
        
        simple_moving_entities = self.get_entities_with_components(PositionComponent, VelocityComponent)
        for entity in simple_moving_entities:
            if entity.has_component(BodyComponent):
                continue
            
            pos_comp = entity.get_component(PositionComponent)
            vel_comp = entity.get_component(VelocityComponent)
            
            if pos_comp and vel_comp:
                pos_comp.x += vel_comp.dx
                pos_comp.y += vel_comp.dy
