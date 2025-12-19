from src.plugins.plugin_interface import PluginModule, PluginMetadata

class BasicEnemyModule(PluginModule):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="BasicEnemy",
            version="1.0.0",
            author="CyberSnake Team",
            description="Basic enemy module with wandering AI snake"
        )
    
    def initialize(self, world, event_bus):
        self.world = world
        self.event_bus = event_bus
        print(f"[BasicEnemy] Module initialized")
    
    def shutdown(self):
        print(f"[BasicEnemy] Module shutdown")

def register_plugin(plugin_manager):
    from .basic_enemy_enemy import WanderingEnemyPlugin
    
    module = BasicEnemyModule()
    plugin_manager.register_module(module)
    
    plugin_manager.register_enemy_plugin(WanderingEnemyPlugin())
