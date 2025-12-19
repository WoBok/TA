from __future__ import annotations
from typing import TYPE_CHECKING, List, Tuple, Optional
import random
import time

from src.ecs.system import System
from src.ecs.components import SpawnComponent

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.plugins.plugin_manager import PluginManager

Vec2 = Tuple[int, int]

class SpawnSystem(System):
    def __init__(self, world: "World", plugin_manager: "PluginManager", grid_width: int, grid_height: int):
        super().__init__(world)
        self.plugin_manager = plugin_manager
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.priority = 5
    
    def update(self, dt: float):
        spawn_entities = self.get_entities_with_components(SpawnComponent)
        current_time = time.time()
        
        for entity in spawn_entities:
            spawn_comp = entity.get_component(SpawnComponent)
            if not spawn_comp:
                continue
            
            if current_time - spawn_comp.last_spawn_time >= spawn_comp.spawn_interval:
                if spawn_comp.max_spawns < 0 or spawn_comp.spawn_count < spawn_comp.max_spawns:
                    self._spawn_entity(spawn_comp)
                    spawn_comp.last_spawn_time = current_time
                    spawn_comp.spawn_count += 1
    
    def _spawn_entity(self, spawn_comp: SpawnComponent):
        position = self._find_empty_position()
        if not position:
            return
        
        if spawn_comp.spawn_type == "food":
            self._spawn_food(position)
        elif spawn_comp.spawn_type == "obstacle":
            self._spawn_obstacle(position)
        elif spawn_comp.spawn_type == "enemy":
            self._spawn_enemy(position)
    
    def _spawn_food(self, position: Vec2):
        food_plugins = self.plugin_manager.get_all_food_plugins()
        if not food_plugins:
            return
        
        weights = [p.get_spawn_weight() for p in food_plugins]
        chosen_plugin = random.choices(food_plugins, weights=weights, k=1)[0]
        
        if chosen_plugin.can_spawn(self.world, position):
            chosen_plugin.create_food(self.world, position)
    
    def _spawn_obstacle(self, position: Vec2):
        obstacle_plugins = self.plugin_manager.get_all_obstacle_plugins()
        if not obstacle_plugins:
            return
        
        weights = [p.get_spawn_weight() for p in obstacle_plugins]
        chosen_plugin = random.choices(obstacle_plugins, weights=weights, k=1)[0]
        chosen_plugin.create_obstacle(self.world, position)
    
    def _spawn_enemy(self, position: Vec2):
        enemy_plugins = self.plugin_manager.get_all_enemy_plugins()
        if not enemy_plugins:
            return
        
        weights = [p.get_spawn_weight() for p in enemy_plugins]
        chosen_plugin = random.choices(enemy_plugins, weights=weights, k=1)[0]
        chosen_plugin.create_enemy(self.world, position)
    
    def _find_empty_position(self) -> Optional[Vec2]:
        from src.ecs.components import PositionComponent, BodyComponent
        
        occupied = set()
        
        for entity in self.world.get_all_entities():
            if entity.has_component(PositionComponent):
                pos_comp = entity.get_component(PositionComponent)
                if pos_comp:
                    occupied.add(pos_comp.pos)
            
            if entity.has_component(BodyComponent):
                body_comp = entity.get_component(BodyComponent)
                if body_comp:
                    occupied.update(body_comp.segments)
        
        possible_positions = []
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                if (x, y) not in occupied:
                    possible_positions.append((x, y))
        
        return random.choice(possible_positions) if possible_positions else None
