from __future__ import annotations
from typing import TYPE_CHECKING

from src.ecs.system import System
from src.ecs.components import EffectComponent, TimerComponent

if TYPE_CHECKING:
    from src.ecs.world import World

class EffectSystem(System):
    def __init__(self, world: "World"):
        super().__init__(world)
        self.priority = 25
    
    def update(self, dt: float):
        effect_entities = self.get_entities_with_components(EffectComponent)
        
        for entity in effect_entities:
            effect_comp = entity.get_component(EffectComponent)
            if not effect_comp:
                continue
            
            effect_comp.elapsed += dt
            
            if effect_comp.elapsed >= effect_comp.duration:
                entity.remove_component(EffectComponent)
        
        timer_entities = self.get_entities_with_components(TimerComponent)
        
        for entity in timer_entities:
            timer_comp = entity.get_component(TimerComponent)
            if not timer_comp:
                continue
            
            timer_comp.elapsed += dt
            
            if timer_comp.is_finished():
                if timer_comp.callback:
                    try:
                        timer_comp.callback()
                    except Exception as e:
                        print(f"Error in timer callback: {e}")
                
                if timer_comp.repeat:
                    timer_comp.elapsed = 0.0
                else:
                    entity.remove_component(TimerComponent)
