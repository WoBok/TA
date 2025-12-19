"""
Plugin Template for CyberSnake
================================

This is a template for creating new plugin modules for CyberSnake.
Replace 'template' with your plugin name throughout all files.

File Structure:
    template_main.py          - Main module registration (this file)
    template_food.py          - Food plugin implementations
    template_obstacle.py      - Obstacle plugin implementations
    template_enemy.py         - Enemy plugin implementations
    template_snakemodify.py   - Snake modifier plugin implementations

You must implement all 4 files, but can leave some empty if your plugin
doesn't affect certain module types.
"""

from src.plugins.plugin_interface import PluginModule, PluginMetadata

class TemplateModule(PluginModule):
    """Main plugin module class."""
    
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="Template",
            version="1.0.0",
            author="Your Name",
            description="Description of what your plugin does"
        )
    
    def initialize(self, world, event_bus):
        """
        Called when the plugin is loaded.
        
        Args:
            world: The ECS world instance
            event_bus: The event bus for subscribing to events
        """
        self.world = world
        self.event_bus = event_bus
        
        # Subscribe to events if needed
        # event_bus.subscribe("event_name", self._on_event)
        
        print(f"[Template] Module initialized")
    
    def shutdown(self):
        """Called when the plugin is unloaded."""
        print(f"[Template] Module shutdown")

def register_plugin(plugin_manager):
    """
    Main registration function called by the plugin manager.
    
    This function should:
    1. Create an instance of your module
    2. Register the module with the plugin manager
    3. Register all food, obstacle, enemy, and snake modifier plugins
    
    Args:
        plugin_manager: The plugin manager instance
    """
    # Import your plugin implementations
    # from .template_food import YourFoodPlugin
    # from .template_obstacle import YourObstaclePlugin
    # from .template_enemy import YourEnemyPlugin
    # from .template_snakemodify import YourSnakeModifierPlugin
    
    # Register the main module
    module = TemplateModule()
    plugin_manager.register_module(module)
    
    # Register individual plugins
    # plugin_manager.register_food_plugin(YourFoodPlugin())
    # plugin_manager.register_obstacle_plugin(YourObstaclePlugin())
    # plugin_manager.register_enemy_plugin(YourEnemyPlugin())
    # plugin_manager.register_snake_modifier_plugin(YourSnakeModifierPlugin())
