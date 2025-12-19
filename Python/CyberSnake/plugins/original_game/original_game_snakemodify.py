from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any
import pygame

from src.plugins.plugin_interface import SnakeModifierPlugin
from src.ecs.components import BodyComponent, SnakeComponent

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

class GrowModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "grow"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        # Growth is handled by not removing tail in movement system
        # Just publish event for tracking
        amount = context.get("amount", 1)
        event_bus.publish("snake_grew", {
            "snake_entity": snake_entity,
            "amount": amount
        })

class EnergyModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "energy"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        amount = context.get("amount", 1)
        event_bus.publish("energy_gained", {
            "snake_entity": snake_entity,
            "amount": amount
        })

class ShrinkModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "shrink"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        body_comp = snake_entity.get_component(BodyComponent)
        if not body_comp or len(body_comp.segments) <= 3:
            return
        
        amount = context.get("amount", 1)
        shrink_amount = min(amount, len(body_comp.segments) - 3)
        
        removed_parts = body_comp.segments[-shrink_amount:]
        body_comp.segments = body_comp.segments[:-shrink_amount]
        
        event_bus.publish("snake_shrunk", {
            "snake_entity": snake_entity,
            "amount": shrink_amount,
            "removed_parts": removed_parts
        })

class GhostModeModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "ghost_mode"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        snake_comp = snake_entity.get_component(SnakeComponent)
        if not snake_comp:
            return
        
        duration_ms = context.get("duration_ms", 5000)
        snake_comp.ghost_mode = True
        snake_comp.ghost_end_time = pygame.time.get_ticks() + duration_ms
        
        event_bus.publish("ghost_mode_activated", {
            "snake_entity": snake_entity,
            "duration_ms": duration_ms
        })
    
    def get_duration(self) -> float:
        return 5.0

class InvertedControlsModifier(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        return "inverted_controls"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        duration_ms = context.get("duration_ms", 5000)
        
        event_bus.publish("inverted_controls_activated", {
            "snake_entity": snake_entity,
            "duration_ms": duration_ms
        })
    
    def get_duration(self) -> float:
        return 5.0
