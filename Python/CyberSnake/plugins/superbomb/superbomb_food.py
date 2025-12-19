from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

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

class SuperBombFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "superbomb"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 100, 0)
        render_comp.glow_color = (255, 150, 0)
        render_comp.radius = 12
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "superbomb"
        food_comp.score_value = 5
        food_comp.growth_amount = 0
        food_comp.energy_value = 0
        food_comp.effects = ["explosion"]
        entity.add_component(food_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("superbomb_food")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        pos_comp = food_entity.get_component(PositionComponent)
        if not pos_comp:
            return
        
        explosion_center = pos_comp.pos
        explosion_radius = 3
        
        event_bus.publish("superbomb_explode", {
            "center": explosion_center,
            "radius": explosion_radius,
            "source": snake_entity
        })
        
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "explosion_shrink",
            "snake_entity": snake_entity,
            "amount": 2
        })
        
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "explosion_clear",
            "snake_entity": snake_entity,
            "center": explosion_center,
            "radius": explosion_radius
        })
        
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 1.0
