from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple

from src.ecs.system import System
from src.ecs.components import (
    PositionComponent,
    BodyComponent,
    CollisionComponent,
    SnakeComponent,
    FoodComponent,
    ObstacleComponent,
    EnemyComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class CollisionSystem(System):
    def __init__(self, world: "World", event_bus: "EventBus"):
        super().__init__(world)
        self.event_bus = event_bus
        self.priority = 20
    
    def update(self, dt: float):
        self._check_food_collisions()
        self._check_obstacle_collisions()
        self._check_enemy_collisions()
        self._check_snake_self_collision()
    
    def _check_food_collisions(self):
        snake_entities = self.get_entities_with_components(SnakeComponent, BodyComponent)
        food_entities = self.get_entities_with_components(FoodComponent, PositionComponent)
        
        for snake_entity in snake_entities:
            body_comp = snake_entity.get_component(BodyComponent)
            if not body_comp or not body_comp.segments:
                continue
            
            snake_head = body_comp.head()
            
            for food_entity in food_entities:
                pos_comp = food_entity.get_component(PositionComponent)
                if not pos_comp:
                    continue
                
                if snake_head == pos_comp.pos:
                    self.event_bus.publish("food_eaten", {
                        "snake_entity": snake_entity,
                        "food_entity": food_entity,
                        "position": snake_head
                    })
    
    def _check_obstacle_collisions(self):
        snake_entities = self.get_entities_with_components(SnakeComponent, BodyComponent)
        obstacle_entities = self.get_entities_with_components(ObstacleComponent, PositionComponent)
        
        for snake_entity in snake_entities:
            snake_comp = snake_entity.get_component(SnakeComponent)
            body_comp = snake_entity.get_component(BodyComponent)
            
            if not body_comp or not body_comp.segments:
                continue
            
            if snake_comp and snake_comp.ghost_mode:
                continue
            
            snake_head = body_comp.head()
            
            for obstacle_entity in obstacle_entities:
                pos_comp = obstacle_entity.get_component(PositionComponent)
                obstacle_comp = obstacle_entity.get_component(ObstacleComponent)
                
                if not pos_comp or not obstacle_comp:
                    continue
                
                if snake_head == pos_comp.pos:
                    self.event_bus.publish("obstacle_collision", {
                        "snake_entity": snake_entity,
                        "obstacle_entity": obstacle_entity,
                        "position": snake_head,
                        "deadly": obstacle_comp.deadly
                    })
    
    def _check_enemy_collisions(self):
        snake_entities = self.get_entities_with_components(SnakeComponent, BodyComponent)
        enemy_entities = self.get_entities_with_components(EnemyComponent, BodyComponent)
        
        for snake_entity in snake_entities:
            snake_comp = snake_entity.get_component(SnakeComponent)
            body_comp = snake_entity.get_component(BodyComponent)
            
            if not body_comp or not body_comp.segments:
                continue
            
            if snake_comp and snake_comp.ghost_mode:
                continue
            
            snake_head = body_comp.head()
            
            for enemy_entity in enemy_entities:
                enemy_body = enemy_entity.get_component(BodyComponent)
                if not enemy_body:
                    continue
                
                if snake_head in enemy_body.segments:
                    self.event_bus.publish("enemy_collision", {
                        "snake_entity": snake_entity,
                        "enemy_entity": enemy_entity,
                        "position": snake_head
                    })
    
    def _check_snake_self_collision(self):
        snake_entities = self.get_entities_with_components(SnakeComponent, BodyComponent)
        
        for snake_entity in snake_entities:
            snake_comp = snake_entity.get_component(SnakeComponent)
            body_comp = snake_entity.get_component(BodyComponent)
            
            if not body_comp or len(body_comp.segments) < 2:
                continue
            
            if snake_comp and snake_comp.ghost_mode:
                continue
            
            snake_head = body_comp.head()
            
            if snake_head in body_comp.segments[1:]:
                self.event_bus.publish("snake_self_collision", {
                    "snake_entity": snake_entity,
                    "position": snake_head
                })
