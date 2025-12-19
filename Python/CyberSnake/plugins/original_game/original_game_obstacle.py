from __future__ import annotations
from typing import TYPE_CHECKING, Tuple
import time
import random
import pygame

from src.plugins.plugin_interface import ObstaclePlugin
from src.ecs.components import (
    PositionComponent, RenderComponent, ObstacleComponent, 
    CollisionComponent, PortalComponent, TrapComponent, TimerComponent
)
from config import OBSTACLE_COLOR, OBSTACLE_GLOW

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.entity import Entity
    from src.ecs.event_bus import EventBus

Vec2 = Tuple[int, int]

class StaticObstaclePlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        return "original_static"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = OBSTACLE_COLOR
        render_comp.glow_color = OBSTACLE_GLOW
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "original_static"
        obstacle_comp.deadly = True
        obstacle_comp.movable = False
        entity.add_component(obstacle_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        entity.add_tag("static_obstacle")
        
        return entity
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        event_bus.publish("game_over", {
            "reason": "Hit obstacle",
            "entity": collider_entity
        })
    
    def is_deadly(self) -> bool:
        return True

class PortalPlugin(ObstaclePlugin):
    def __init__(self):
        self.portal_pairs = {}
    
    def get_obstacle_type(self) -> str:
        return "portal"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 140, 0)
        render_comp.glow_color = (255, 180, 100)
        render_comp.radius = 12
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "portal"
        obstacle_comp.deadly = False
        obstacle_comp.movable = False
        entity.add_component(obstacle_comp)
        
        portal_comp = PortalComponent()
        portal_comp.portal_type = "orange"
        portal_comp.cooldown = 0.5
        portal_comp.last_use_time = 0.0
        entity.add_component(portal_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        entity.add_tag("portal")
        
        return entity
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        portal_comp = obstacle_entity.get_component(PortalComponent)
        
        if portal_comp and portal_comp.linked_portal_id:
            current_time = time.time()
            if current_time - portal_comp.last_use_time >= portal_comp.cooldown:
                linked_portal = world.get_entity(portal_comp.linked_portal_id)
                if linked_portal:
                    linked_pos = linked_portal.get_component(PositionComponent)
                    from src.ecs.components import BodyComponent
                    collider_body = collider_entity.get_component(BodyComponent)
                    
                    if linked_pos and collider_body and collider_body.segments:
                        collider_body.segments[0] = linked_pos.pos
                        portal_comp.last_use_time = current_time
                        
                        event_bus.publish("portal_used", {
                            "entity": collider_entity,
                            "from": obstacle_entity.get_component(PositionComponent).pos,
                            "to": linked_pos.pos
                        })
    
    def is_deadly(self) -> bool:
        return False

class SpikeTrapPlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        return "spike_trap"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 80, 200)
        render_comp.glow_color = (255, 120, 220)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "spike_trap"
        obstacle_comp.deadly = True
        obstacle_comp.movable = False
        entity.add_component(obstacle_comp)
        
        trap_comp = TrapComponent()
        trap_comp.trap_type = "spike"
        trap_comp.damage = 1
        trap_comp.active = True
        trap_comp.trigger_delay = 0.0
        entity.add_component(trap_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        entity.add_tag("trap")
        entity.add_tag("spike_trap")
        
        return entity
    
    def update_obstacle(self, world: "World", obstacle_entity: "Entity", dt: float) -> None:
        trap_comp = obstacle_entity.get_component(TrapComponent)
        if trap_comp:
            t = int(time.time() * 1000) % 1000
            trap_comp.active = t >= 500
            
            render_comp = obstacle_entity.get_component(RenderComponent)
            if render_comp:
                if trap_comp.active:
                    render_comp.color = (255, 80, 200)
                else:
                    render_comp.color = (140, 60, 140)
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        trap_comp = obstacle_entity.get_component(TrapComponent)
        if trap_comp and trap_comp.active:
            event_bus.publish("game_over", {
                "reason": "Hit spike trap",
                "entity": collider_entity
            })
    
    def is_deadly(self) -> bool:
        return True

class LavaPoolPlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        return "lava_pool"
    
    def create_obstacle(self, world: "World", position: Vec2) -> "Entity":
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 80, 0)
        render_comp.glow_color = (255, 120, 50)
        render_comp.radius = 12
        render_comp.shape = "square"
        render_comp.layer = 1
        render_comp.alpha = 180
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "lava_pool"
        obstacle_comp.deadly = True
        obstacle_comp.movable = False
        entity.add_component(obstacle_comp)
        
        trap_comp = TrapComponent()
        trap_comp.trap_type = "lava"
        trap_comp.damage = 1
        trap_comp.active = False
        entity.add_component(trap_comp)
        
        timer_comp = TimerComponent()
        timer_comp.duration = random.uniform(3.0, 5.0)
        timer_comp.elapsed = 0.0
        timer_comp.repeat = True
        entity.add_component(timer_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        entity.add_tag("trap")
        entity.add_tag("lava_pool")
        
        return entity
    
    def update_obstacle(self, world: "World", obstacle_entity: "Entity", dt: float) -> None:
        timer_comp = obstacle_entity.get_component(TimerComponent)
        trap_comp = obstacle_entity.get_component(TrapComponent)
        
        if timer_comp and trap_comp:
            timer_comp.elapsed += dt
            
            if timer_comp.elapsed >= timer_comp.duration:
                trap_comp.active = not trap_comp.active
                timer_comp.elapsed = 0.0
                timer_comp.duration = random.uniform(3.0, 5.0)
                
                render_comp = obstacle_entity.get_component(RenderComponent)
                if render_comp:
                    if trap_comp.active:
                        render_comp.color = (255, 80, 0)
                        render_comp.alpha = 180
                    else:
                        render_comp.color = (120, 30, 0)
                        render_comp.alpha = 100
    
    def on_collision(self, world: "World", event_bus: "EventBus", obstacle_entity: "Entity", collider_entity: "Entity") -> None:
        trap_comp = obstacle_entity.get_component(TrapComponent)
        if trap_comp and trap_comp.active:
            event_bus.publish("game_over", {
                "reason": "Fell into lava",
                "entity": collider_entity
            })
    
    def is_deadly(self) -> bool:
        return True
