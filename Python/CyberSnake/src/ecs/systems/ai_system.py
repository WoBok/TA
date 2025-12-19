from __future__ import annotations
from typing import TYPE_CHECKING
import time

from src.ecs.system import System
from src.ecs.components import AIComponent, EnemyComponent

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.plugins.plugin_manager import PluginManager

class AISystem(System):
    def __init__(self, world: "World", plugin_manager: "PluginManager"):
        super().__init__(world)
        self.plugin_manager = plugin_manager
        self.priority = 15
    
    def update(self, dt: float):
        ai_entities = self.get_entities_with_components(AIComponent, EnemyComponent)
        current_time = time.time()
        
        for entity in ai_entities:
            ai_comp = entity.get_component(AIComponent)
            enemy_comp = entity.get_component(EnemyComponent)
            
            if not ai_comp or not enemy_comp:
                continue
            
            if current_time - ai_comp.last_update >= ai_comp.update_interval:
                enemy_plugin = self.plugin_manager.get_enemy_plugin(enemy_comp.enemy_type)
                if enemy_plugin:
                    enemy_plugin.update_ai(self.world, entity, dt)
                    ai_comp.last_update = current_time
