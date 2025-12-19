"""
Snake Modifier Plugin Template
===============================

Implement modifiers that affect the snake's behavior or state.
Each modifier should define:
- What it modifies (length, speed, abilities, etc.)
- Duration (if temporary)
- Visual effects
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Dict, Any

from src.plugins.plugin_interface import SnakeModifierPlugin
from src.ecs.components import BodyComponent, SnakeComponent

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

class YourSnakeModifierPlugin(SnakeModifierPlugin):
    """Example snake modifier plugin implementation."""
    
    def get_modifier_type(self) -> str:
        """Return unique identifier for this modifier type."""
        return "your_modifier_type"
    
    def apply_modifier(self, world: "World", event_bus: "EventBus", snake_entity: "Entity", context: Dict[str, Any]) -> None:
        """
        Apply the modifier to the snake.
        
        Args:
            world: The ECS world
            event_bus: Event bus for publishing events
            snake_entity: The snake entity to modify
            context: Additional context data (e.g., amount, duration)
        """
        body_comp = snake_entity.get_component(BodyComponent)
        snake_comp = snake_entity.get_component(SnakeComponent)
        
        if not body_comp or not snake_comp:
            return
        
        # Example: Grow the snake
        amount = context.get("amount", 1)
        # Growth is handled automatically by not removing tail segments
        
        # Example: Activate ghost mode
        # snake_comp.ghost_mode = True
        # snake_comp.ghost_end_time = pygame.time.get_ticks() + 5000
        
        # Publish event for other systems to react
        event_bus.publish("snake_modified", {
            "snake_entity": snake_entity,
            "modifier_type": self.get_modifier_type(),
            "context": context
        })
    
    def can_apply(self, world: "World", snake_entity: "Entity") -> bool:
        """
        Check if this modifier can be applied to the snake.
        Optional - default returns True.
        """
        return True
    
    def get_duration(self) -> float:
        """
        Return duration in seconds for temporary effects.
        Return 0.0 for permanent effects.
        """
        return 0.0
    
    def on_modifier_end(self, world: "World", snake_entity: "Entity") -> None:
        """
        Called when a temporary modifier expires.
        Optional - only implement for temporary effects.
        """
        pass
