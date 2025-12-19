"""
Obstacle Plugin Template
=========================

Implement obstacle types that block or affect the snake.
Each obstacle type should define:
- Visual appearance
- Behavior (static, moving, etc.)
- What happens on collision
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from src.plugins.plugin_interface import ObstaclePlugin
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    ObstacleComponent,
    CollisionComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class YourObstaclePlugin(ObstaclePlugin):
    """Example obstacle plugin implementation."""
    
    def get_obstacle_type(self) -> str:
        """Return unique identifier for this obstacle type."""
        return "your_obstacle_type"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        """
        Create an obstacle entity at the given position.
        
        Args:
            world: The ECS world
            position: Grid position (x, y)
            
        Returns:
            The created obstacle entity
        """
        entity = world.create_entity()
        
        # Position component
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        # Render component
        render_comp = RenderComponent()
        render_comp.color = (200, 0, 255)  # Purple
        render_comp.glow_color = (150, 0, 200)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        # Obstacle component
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "your_obstacle_type"
        obstacle_comp.deadly = True  # Does it kill the snake?
        obstacle_comp.movable = False  # Can it move?
        entity.add_component(obstacle_comp)
        
        # Collision component
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        # Tags
        entity.add_tag("obstacle")
        entity.add_tag("your_obstacle_type")
        
        return entity
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        """
        Called when something collides with this obstacle.
        
        Args:
            world: The ECS world
            event_bus: Event bus for publishing events
            obstacle_entity: The obstacle entity
            collider_entity: The entity that collided (usually the snake)
        """
        obstacle_comp = obstacle_entity.get_component(ObstacleComponent)
        
        if obstacle_comp and obstacle_comp.deadly:
            # Trigger game over
            event_bus.publish("game_over", {
                "reason": "Hit obstacle",
                "entity": collider_entity
            })
    
    def update_obstacle(self, world: "World", obstacle_entity: "Entity", dt: float) -> None:
        """
        Update obstacle behavior each frame.
        Optional - only implement if obstacle needs to move or change.
        
        Args:
            world: The ECS world
            obstacle_entity: The obstacle entity
            dt: Delta time in seconds
        """
        pass
    
    def get_spawn_weight(self) -> float:
        """Return spawn weight (higher = more likely to spawn)."""
        return 1.0
    
    def is_deadly(self) -> bool:
        """Return True if this obstacle kills the snake on contact."""
        return True
