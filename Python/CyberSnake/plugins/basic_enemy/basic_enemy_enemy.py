from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import random

from src.plugins.plugin_interface import EnemyPlugin
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    BodyComponent,
    VelocityComponent,
    EnemyComponent,
    AIComponent,
    CollisionComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class WanderingEnemyPlugin(EnemyPlugin):
    def get_enemy_type(self) -> str:
        return "wandering"
    
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        body_comp = BodyComponent()
        body_comp.segments = [position, (position[0]-1, position[1]), (position[0]-2, position[1])]
        entity.add_component(body_comp)
        
        vel_comp = VelocityComponent()
        vel_comp.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        entity.add_component(vel_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 120, 60)
        render_comp.glow_color = (255, 150, 100)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 2
        entity.add_component(render_comp)
        
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "wandering"
        enemy_comp.ai_behavior = "wander"
        enemy_comp.damage = 1
        enemy_comp.is_boss = False
        entity.add_component(enemy_comp)
        
        ai_comp = AIComponent()
        ai_comp.behavior = "wander"
        ai_comp.update_interval = 0.1
        entity.add_component(ai_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        entity.add_tag("enemy")
        entity.add_tag("wandering_enemy")
        
        return entity
    
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        vel_comp = enemy_entity.get_component(VelocityComponent)
        if not vel_comp:
            return
        
        if random.random() < 0.25:
            vel_comp.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
    
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        event_bus.publish("game_over", {
            "reason": "Hit enemy",
            "entity": collider_entity
        })
    
    def is_boss(self) -> bool:
        return False
    
    def get_spawn_weight(self) -> float:
        return 5.0
