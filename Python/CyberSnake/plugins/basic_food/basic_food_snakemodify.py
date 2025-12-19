from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any

from src.plugins.plugin_interface import SnakeModifierPlugin
from src.ecs.components import BodyComponent, SnakeComponent

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

class GrowSnakeModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "grow"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        body_comp = snake_entity.get_component(BodyComponent)
        if not body_comp or not body_comp.segments:
            return
        
        amount = context.get("amount", 1)
        
        for _ in range(amount):
            pass
        
        event_bus.publish("snake_grew", {
            "snake_entity": snake_entity,
            "amount": amount
        })

class EnergyBoostModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "energy_boost"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        amount = context.get("amount", 1)
        
        event_bus.publish("energy_gained", {
            "snake_entity": snake_entity,
            "amount": amount
        })
