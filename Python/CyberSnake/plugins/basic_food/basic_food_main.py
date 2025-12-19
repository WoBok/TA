from src.plugins.plugin_interface import PluginModule, PluginMetadata

class BasicFoodModule(PluginModule):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="BasicFood",
            version="1.0.0",
            author="CyberSnake Team",
            description="Basic food module with normal and energy food types"
        )
    
    def initialize(self, world, event_bus):
        self.world = world
        self.event_bus = event_bus
        print(f"[BasicFood] Module initialized")
    
    def shutdown(self):
        print(f"[BasicFood] Module shutdown")

def register_plugin(plugin_manager):
    from .basic_food_food import NormalFoodPlugin, EnergyFoodPlugin
    from .basic_food_snakemodify import GrowSnakeModifier, EnergyBoostModifier
    
    module = BasicFoodModule()
    plugin_manager.register_module(module)
    
    plugin_manager.register_food_plugin(NormalFoodPlugin())
    plugin_manager.register_food_plugin(EnergyFoodPlugin())
    
    plugin_manager.register_snake_modifier_plugin(GrowSnakeModifier())
    plugin_manager.register_snake_modifier_plugin(EnergyBoostModifier())
