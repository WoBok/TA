"""
Enemy Plugin Template
======================

Implement enemy types with AI behavior.
Each enemy type should define:
- Visual appearance
- AI behavior
- What happens on collision
"""

from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Dict, Any
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

class YourEnemyPlugin(EnemyPlugin):
    """Example enemy plugin implementation."""
    
    def get_enemy_type(self) -> str:
        """Return unique identifier for this enemy type."""
        return "your_enemy_type"
    
    def create_enemy(self, world: "World", position: Vec2) -> "Entity":
        """
        Create an enemy entity at the given position.
        
        Args:
            world: The ECS world
            position: Grid position (x, y)
            
        Returns:
            The created enemy entity
        """
        entity = world.create_entity()
        
        # Body component (for snake-like enemies)
        body_comp = BodyComponent()
        body_comp.segments = [position, (position[0]-1, position[1])]
        entity.add_component(body_comp)
        
        # Velocity component
        vel_comp = VelocityComponent()
        vel_comp.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        entity.add_component(vel_comp)
        
        # Render component
        render_comp = RenderComponent()
        render_comp.color = (255, 120, 60)  # Orange
        render_comp.glow_color = (255, 150, 100)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 2
        entity.add_component(render_comp)
        
        # Enemy component
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "your_enemy_type"
        enemy_comp.ai_behavior = "chase"  # or "wander", "patrol", etc.
        enemy_comp.damage = 1
        enemy_comp.is_boss = False
        entity.add_component(enemy_comp)
        
        # AI component
        ai_comp = AIComponent()
        ai_comp.behavior = "chase"
        ai_comp.update_interval = 0.1  # Update AI every 0.1 seconds
        entity.add_component(ai_comp)
        
        # Collision component
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        # Tags
        entity.add_tag("enemy")
        entity.add_tag("your_enemy_type")
        
        return entity
    
    def update_ai(self, world: "World", enemy_entity: "Entity", dt: float) -> None:
        """
        Update enemy AI behavior.
        
        Args:
            world: The ECS world
            enemy_entity: The enemy entity
            dt: Delta time in seconds
        """
        vel_comp = enemy_entity.get_component(VelocityComponent)
        if not vel_comp:
            return
        
        # Example: Random wandering
        if random.random() < 0.1:
            vel_comp.direction = random.choice([(0, 1), (0, -1), (1, 0), (-1, 0)])
        
        # Example: Chase player
        # player_entities = world.get_entities_with_tag("player")
        # if player_entities:
        #     player = player_entities[0]
        #     # Calculate direction to player and move towards them
    
    def on_collision(self, world: "World", event_bus: "EventBus", enemy_entity: "Entity", collider_entity: "Entity") -> None:
        """
        Called when something collides with this enemy.
        
        Args:
            world: The ECS world
            event_bus: Event bus for publishing events
            enemy_entity: The enemy entity
            collider_entity: The entity that collided (usually the snake)
        """
        # Trigger game over
        event_bus.publish("game_over", {
            "reason": "Hit enemy",
            "entity": collider_entity
        })
    
    def is_boss(self) -> bool:
        """Return True if this is a boss enemy."""
        return False
    
    def get_spawn_weight(self) -> float:
        """Return spawn weight (higher = more likely to spawn)."""
        return 1.0
    
    def get_spawn_conditions(self) -> Dict[str, Any]:
        """
        Return conditions for spawning this enemy.
        Optional - can specify minimum score, etc.
        """
        return {}
