from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

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

class StunnedEnemyPlugin(EnemyPlugin):
    def get_enemy_type(self) -> str:
        return "stunned"
    
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        body_comp = BodyComponent()
        body_comp.segments = [position]
        entity.add_component(body_comp)
        
        vel_comp = VelocityComponent()
        vel_comp.direction = (0, 0)
        entity.add_component(vel_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (200, 200, 100)
        render_comp.glow_color = (150, 150, 50)
        render_comp.radius = 8
        render_comp.shape = "circle"
        render_comp.layer = 2
        entity.add_component(render_comp)
        
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "stunned"
        enemy_comp.ai_behavior = "stunned"
        enemy_comp.damage = 0
        enemy_comp.is_boss = False
        entity.add_component(enemy_comp)
        
        ai_comp = AIComponent()
        ai_comp.behavior = "stunned"
        ai_comp.update_interval = 1.0
        entity.add_component(ai_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        entity.add_tag("enemy")
        entity.add_tag("stunned_enemy")
        
        return entity
    
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        pass
    
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        pass
    
    def is_boss(self) -> bool:
        return False
    
    def get_spawn_weight(self) -> float:
        return 0.0
