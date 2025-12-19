from __future__ import annotations
from typing import TYPE_CHECKING, Tuple, Dict, Any

from src.plugins.plugin_interface import FoodPlugin
from src.ecs.components import (
    PositionComponent,
    RenderComponent,
    FoodComponent,
    CollisionComponent
)
from config import FOOD_COLOR, FOOD_GLOW, ENERGY_FOOD_COLOR, ENERGY_GLOW

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class NormalFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "normal"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = FOOD_COLOR
        render_comp.glow_color = FOOD_GLOW
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "normal"
        food_comp.score_value = 1
        food_comp.growth_amount = 1
        food_comp.energy_value = 0
        entity.add_component(food_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("normal_food")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "grow",
            "snake_entity": snake_entity,
            "amount": 1
        })
        
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 10.0

class EnergyFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "energy"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = ENERGY_FOOD_COLOR
        render_comp.glow_color = ENERGY_GLOW
        render_comp.radius = 10
        render_comp.shape = "square"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "energy"
        food_comp.score_value = 0
        food_comp.growth_amount = 0
        food_comp.energy_value = 1
        entity.add_component(food_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("energy_food")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "energy_boost",
            "snake_entity": snake_entity,
            "amount": 1
        })
        
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 2.0
