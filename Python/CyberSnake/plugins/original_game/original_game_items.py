from __future__ import annotations
from typing import TYPE_CHECKING, Tuple

from src.plugins.plugin_interface import FoodPlugin
from src.ecs.components import (
    PositionComponent, RenderComponent, FoodComponent, 
    CollisionComponent, ItemComponent
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class MagnetItemPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "magnet_item"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 255, 0)
        render_comp.glow_color = (255, 255, 100)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "magnet_item"
        food_comp.score_value = 0
        food_comp.effects = ["magnet"]
        entity.add_component(food_comp)
        
        item_comp = ItemComponent()
        item_comp.item_type = "magnet"
        item_comp.duration = 5.0
        entity.add_component(item_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("item")
        entity.add_tag("magnet")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        event_bus.publish("magnet_activated", {
            "snake_entity": snake_entity,
            "duration_ms": 5000,
            "radius_cells": 5
        })
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 1.0

class BombItemPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "bomb_item"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (40, 40, 40)
        render_comp.glow_color = (100, 100, 100)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "bomb_item"
        food_comp.score_value = 0
        food_comp.effects = ["bomb"]
        entity.add_component(food_comp)
        
        item_comp = ItemComponent()
        item_comp.item_type = "bomb"
        entity.add_component(item_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("item")
        entity.add_tag("bomb")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        pos_comp = food_entity.get_component(PositionComponent)
        if pos_comp:
            # Clear all obstacles
            for entity in world.get_entities_with_tag("obstacle"):
                entity.destroy()
            
            event_bus.publish("bomb_exploded", {
                "snake_entity": snake_entity,
                "position": pos_comp.pos
            })
        
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 1.0

class ScissorsItemPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "scissors_item"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (0, 255, 127)
        render_comp.glow_color = (50, 255, 150)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "scissors_item"
        food_comp.score_value = 0
        food_comp.effects = ["shrink"]
        entity.add_component(food_comp)
        
        item_comp = ItemComponent()
        item_comp.item_type = "scissors"
        entity.add_component(item_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("item")
        entity.add_tag("scissors")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "shrink",
            "snake_entity": snake_entity,
            "amount": 4
        })
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 1.0

class ScoreBoostItemPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "score_boost_item"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (80, 180, 255)
        render_comp.glow_color = (120, 200, 255)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "score_boost_item"
        food_comp.score_value = 25
        food_comp.effects = ["score_boost"]
        entity.add_component(food_comp)
        
        item_comp = ItemComponent()
        item_comp.item_type = "score_boost"
        entity.add_component(item_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("item")
        entity.add_tag("score_boost")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        event_bus.publish("score_boost_collected", {
            "snake_entity": snake_entity,
            "bonus": 25
        })
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 1.0

class RottenAppleItemPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "rotten_apple_item"
    
    def create_food(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (100, 50, 50)
        render_comp.glow_color = (120, 70, 70)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "rotten_apple_item"
        food_comp.score_value = 0
        food_comp.effects = ["inverted"]
        entity.add_component(food_comp)
        
        item_comp = ItemComponent()
        item_comp.item_type = "rotten_apple"
        item_comp.duration = 5.0
        entity.add_component(item_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        entity.add_tag("food")
        entity.add_tag("item")
        entity.add_tag("rotten_apple")
        
        return entity
    
    def on_food_eaten(self, world: "World", event_bus: "EventBus", food_entity: "Entity", snake_entity: "Entity") -> None:
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "inverted_controls",
            "snake_entity": snake_entity,
            "duration_ms": 5000
        })
        food_entity.destroy()
    
    def get_spawn_weight(self) -> float:
        return 1.0
