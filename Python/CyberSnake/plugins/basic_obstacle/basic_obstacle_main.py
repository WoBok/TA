from src.plugins.plugin_interface import PluginModule, PluginMetadata

class BasicObstacleModule(PluginModule):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="BasicObstacle",
            version="1.0.0",
            author="CyberSnake Team",
            description="Basic obstacle module with static obstacles"
        )
    
    def initialize(self, world, event_bus):
        self.world = world
        self.event_bus = event_bus
        print(f"[BasicObstacle] Module initialized")
    
    def shutdown(self):
        print(f"[BasicObstacle] Module shutdown")

def register_plugin(plugin_manager):
    from .basic_obstacle_obstacle import StaticObstaclePlugin
    
    module = BasicObstacleModule()
    plugin_manager.register_module(module)
    
    plugin_manager.register_obstacle_plugin(StaticObstaclePlugin())
