from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any, Tuple

from src.plugins.plugin_interface import SnakeModifierPlugin
from src.ecs.components import (
    BodyComponent,
    PositionComponent,
    ObstacleComponent,
    EnemyComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class ExplosionShrinkModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "explosion_shrink"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        body_comp = snake_entity.get_component(BodyComponent)
        if not body_comp or len(body_comp.segments) <= 3:
            return
        
        amount = context.get("amount", 2)
        shrink_amount = min(amount, len(body_comp.segments) - 3)
        
        body_comp.segments = body_comp.segments[:-shrink_amount]
        
        event_bus.publish("snake_shrunk", {
            "snake_entity": snake_entity,
            "amount": shrink_amount
        })

class ExplosionClearModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "explosion_clear"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        center = context.get("center", (0, 0))
        radius = context.get("radius", 3)
        
        entities_to_destroy = []
        
        for entity in world.get_all_entities():
            if entity == snake_entity:
                continue
            
            pos_comp = entity.get_component(PositionComponent)
            if not pos_comp:
                continue
            
            distance = abs(pos_comp.x - center[0]) + abs(pos_comp.y - center[1])
            
            if distance <= radius:
                if entity.has_component(ObstacleComponent) or entity.has_component(EnemyComponent):
                    entities_to_destroy.append(entity)
        
        for entity in entities_to_destroy:
            entity.destroy()
        
        event_bus.publish("explosion_cleared", {
            "center": center,
            "radius": radius,
            "cleared_count": len(entities_to_destroy)
        })
