"""
Original Game Features Plugin
Restores all original CyberSnake gameplay features using the new ECS architecture
"""

from src.plugins.plugin_interface import PluginModule, PluginMetadata

class OriginalGameModule(PluginModule):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="OriginalGame",
            version="1.0.0",
            author="CyberSnake Team",
            description="Complete original game features: items, portals, traps, boss, particles, effects"
        )
    
    def initialize(self, world, event_bus):
        self.world = world
        self.event_bus = event_bus
        print(f"[OriginalGame] Module initialized")
    
    def shutdown(self):
        print(f"[OriginalGame] Module shutdown")

def register_plugin(plugin_manager):
    from .original_game_food import OriginalFoodPlugin, OriginalEnergyFoodPlugin
    from .original_game_obstacle import (
        StaticObstaclePlugin, PortalPlugin, SpikeTrapPlugin, LavaPoolPlugin
    )
    from .original_game_enemy import (
        AISnakePlugin, GhostHunterPlugin, BossPlugin
    )
    from .original_game_snakemodify import (
        GrowModifier, EnergyModifier, ShrinkModifier, 
        GhostModeModifier, InvertedControlsModifier
    )
    from .original_game_items import (
        MagnetItemPlugin, BombItemPlugin, ScissorsItemPlugin,
        ScoreBoostItemPlugin, RottenAppleItemPlugin
    )
    
    module = OriginalGameModule()
    plugin_manager.register_module(module)
    
    # Register food plugins
    plugin_manager.register_food_plugin(OriginalFoodPlugin())
    plugin_manager.register_food_plugin(OriginalEnergyFoodPlugin())
    
    # Register obstacle plugins
    plugin_manager.register_obstacle_plugin(StaticObstaclePlugin())
    plugin_manager.register_obstacle_plugin(PortalPlugin())
    plugin_manager.register_obstacle_plugin(SpikeTrapPlugin())
    plugin_manager.register_obstacle_plugin(LavaPoolPlugin())
    
    # Register enemy plugins
    plugin_manager.register_enemy_plugin(AISnakePlugin())
    plugin_manager.register_enemy_plugin(GhostHunterPlugin())
    plugin_manager.register_enemy_plugin(BossPlugin())
    
    # Register snake modifiers
    plugin_manager.register_snake_modifier_plugin(GrowModifier())
    plugin_manager.register_snake_modifier_plugin(EnergyModifier())
    plugin_manager.register_snake_modifier_plugin(ShrinkModifier())
    plugin_manager.register_snake_modifier_plugin(GhostModeModifier())
    plugin_manager.register_snake_modifier_plugin(InvertedControlsModifier())
    
    # Register item plugins
    plugin_manager.register_food_plugin(MagnetItemPlugin())
    plugin_manager.register_food_plugin(BombItemPlugin())
    plugin_manager.register_food_plugin(ScissorsItemPlugin())
    plugin_manager.register_food_plugin(ScoreBoostItemPlugin())
    plugin_manager.register_food_plugin(RottenAppleItemPlugin())
