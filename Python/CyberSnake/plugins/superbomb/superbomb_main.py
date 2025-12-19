from src.plugins.plugin_interface import PluginModule, PluginMetadata

class SuperBombModule(PluginModule):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="SuperBomb",
            version="1.0.0",
            author="CyberSnake Team",
            description="SuperBomb module - explosive food that clears obstacles, enemies, and shrinks snake"
        )
    
    def initialize(self, world, event_bus):
        self.world = world
        self.event_bus = event_bus
        
        event_bus.subscribe("superbomb_explode", self._on_explosion)
        
        print(f"[SuperBomb] Module initialized")
    
    def _on_explosion(self, payload):
        center = payload.get("center")
        radius = payload.get("radius", 3)
        
        print(f"[SuperBomb] Explosion at {center} with radius {radius}")
    
    def shutdown(self):
        print(f"[SuperBomb] Module shutdown")

def register_plugin(plugin_manager):
    from .superbomb_food import SuperBombFoodPlugin
    from .superbomb_obstacle import ExplosionDebrisPlugin
    from .superbomb_enemy import StunnedEnemyPlugin
    from .superbomb_snakemodify import ExplosionShrinkModifier, ExplosionClearModifier
    
    module = SuperBombModule()
    plugin_manager.register_module(module)
    
    plugin_manager.register_food_plugin(SuperBombFoodPlugin())
    
    plugin_manager.register_obstacle_plugin(ExplosionDebrisPlugin())
    
    plugin_manager.register_enemy_plugin(StunnedEnemyPlugin())
    
    plugin_manager.register_snake_modifier_plugin(ExplosionShrinkModifier())
    plugin_manager.register_snake_modifier_plugin(ExplosionClearModifier())
