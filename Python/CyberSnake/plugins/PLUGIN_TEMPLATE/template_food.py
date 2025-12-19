"""
Food Plugin Template
====================

Implement food types that can be eaten by the snake.
Each food type should define:
- What it looks like (color, shape, size)
- What happens when eaten
- How often it spawns (spawn weight)
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Dict, Any

from src.plugins.plugin_interface import FoodPlugin
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    FoodComponent,
    CollisionComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class YourFoodPlugin(FoodPlugin):
    """Example food plugin implementation."""
    
    def get_food_type(self) -> str:
        """Return unique identifier for this food type."""
        return "your_food_type"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        """
        Create a food entity at the given position.
        
        Args:
            world: The ECS world
            position: Grid position (x, y)
            
        Returns:
            The created food entity
        """
        entity = world.create_entity()
        
        # Position component
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        # Render component (visual appearance)
        render_comp = RenderComponent()
        render_comp.color = (255, 0, 0)  # Red
        render_comp.glow_color = (255, 100, 100)  # Light red glow
        render_comp.radius = 10
        render_comp.shape = "circle"  # or "square"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        # Food component (game logic)
        food_comp = FoodComponent()
        food_comp.food_type = "your_food_type"
        food_comp.score_value = 1
        food_comp.growth_amount = 1
        food_comp.energy_value = 0
        food_comp.effects = []  # Optional effects list
        entity.add_component(food_comp)
        
        # Collision component
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        # Tags for easy querying
        entity.add_tag("food")
        entity.add_tag("your_food_type")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        """
        Called when this food is eaten by the snake.
        
        Args:
            world: The ECS world
            event_bus: Event bus for publishing events
            food_entity: The food entity that was eaten
            snake_entity: The snake entity that ate the food
        """
        # Apply effects to the snake
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "your_modifier_type",
            "snake_entity": snake_entity,
            "amount": 1
        })
        
        # Destroy the food entity
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        """
        Return spawn weight (higher = more likely to spawn).
        Default is 1.0.
        """
        return 1.0
    
    def can_spawn(self, world: "World", position: Vec2) -> bool:
        """
        Check if this food can spawn at the given position.
        Optional - default returns True.
        """
        return True
