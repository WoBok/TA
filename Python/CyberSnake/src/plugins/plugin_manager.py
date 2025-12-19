from __future__ import annotations
from typing import TYPE_CHECKING, Dict, List, Type, Optional, Any
import os
import sys
import importlib
import importlib.util
import types
from pathlib import Path

from .plugin_interface import (
    PluginModule,
    FoodPlugin,
    ObstaclePlugin,
    EnemyPlugin,
    SnakeModifierPlugin
)

if TYPE_CHECKING:
    from src.ecs.world import World
    from src.ecs.event_bus import EventBus

class PluginManager:
    def __init__(self, world: "World", event_bus: "EventBus"):
        self.world = world
        self.event_bus = event_bus
        
        self.modules: Dict[str, PluginModule] = {}
        self.food_plugins: Dict[str, FoodPlugin] = {}
        self.obstacle_plugins: Dict[str, ObstaclePlugin] = {}
        self.enemy_plugins: Dict[str, EnemyPlugin] = {}
        self.snake_modifier_plugins: Dict[str, SnakeModifierPlugin] = {}
        
        self.plugin_directories: List[Path] = []
    
    def add_plugin_directory(self, directory: str | Path) -> None:
        path = Path(directory)
        if path.exists() and path.is_dir():
            self.plugin_directories.append(path)
    
    def discover_plugins(self) -> None:
        for plugin_dir in self.plugin_directories:
            self._scan_directory(plugin_dir)
    
    def _scan_directory(self, directory: Path) -> None:
        if not directory.exists():
            return
        
        for item in directory.iterdir():
            if item.is_dir() and not item.name.startswith('_') and not item.name.startswith('.'):
                if item.name == "PLUGIN_TEMPLATE":
                    continue
                self._load_plugin_module(item)
    
    def _load_plugin_module(self, module_path: Path) -> None:
        module_name = module_path.name
 
        # Ensure top-level 'plugins' package is importable
        plugins_root = module_path.parent
        if str(plugins_root.parent) not in sys.path:
            sys.path.insert(0, str(plugins_root.parent))

        # Ensure 'plugins' exists in sys.modules as a package
        if "plugins" not in sys.modules:
            plugins_pkg = types.ModuleType("plugins")
            plugins_pkg.__path__ = [str(plugins_root)]  # type: ignore[attr-defined]
            sys.modules["plugins"] = plugins_pkg
        else:
            plugins_pkg = sys.modules["plugins"]
            try:
                existing_paths = list(getattr(plugins_pkg, "__path__", []))
                if str(plugins_root) not in existing_paths:
                    existing_paths.append(str(plugins_root))
                    plugins_pkg.__path__ = existing_paths  # type: ignore[attr-defined]
            except Exception:
                pass

        # Ensure 'plugins.<module_name>' exists as a package for relative imports
        plugin_pkg_name = f"plugins.{module_name}"
        if plugin_pkg_name not in sys.modules:
            plugin_pkg = types.ModuleType(plugin_pkg_name)
            plugin_pkg.__path__ = [str(module_path)]  # type: ignore[attr-defined]
            sys.modules[plugin_pkg_name] = plugin_pkg

        main_file = module_path / f"{module_name}_main.py"
        if not main_file.exists():
            # Support plugins that use __init__.py as entry
            main_file = module_path / "__init__.py"
            if not main_file.exists():
                print(f"Warning: No main file found for plugin module {module_name}")
                return
        
        try:
            # Load entry module as a submodule of the plugin package:
            # plugins.<module_name>.<module_name>_main
            entry_mod_name = f"{plugin_pkg_name}.{main_file.stem}"
            spec = importlib.util.spec_from_file_location(entry_mod_name, main_file)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[entry_mod_name] = module
                spec.loader.exec_module(module)
                
                if hasattr(module, 'register_plugin'):
                    module.register_plugin(self)
                    print(f"Loaded plugin module: {module_name}")
                else:
                    print(f"Warning: Plugin module {module_name} has no register_plugin function")
        
        except Exception as e:
            print(f"Error loading plugin module {module_name}: {e}")
            import traceback
            traceback.print_exc()
    
    def register_module(self, module: PluginModule) -> None:
        metadata = module.get_metadata()
        if metadata.name in self.modules:
            print(f"Warning: Module {metadata.name} already registered, skipping")
            return
        
        self.modules[metadata.name] = module
        module.initialize(self.world, self.event_bus)
        print(f"Registered module: {metadata.name} v{metadata.version}")
    
    def register_food_plugin(self, plugin: FoodPlugin) -> None:
        food_type = plugin.get_food_type()
        if food_type in self.food_plugins:
            print(f"Warning: Food plugin {food_type} already registered, skipping")
            return
        
        self.food_plugins[food_type] = plugin
        print(f"Registered food plugin: {food_type}")
    
    def register_obstacle_plugin(self, plugin: ObstaclePlugin) -> None:
        obstacle_type = plugin.get_obstacle_type()
        if obstacle_type in self.obstacle_plugins:
            print(f"Warning: Obstacle plugin {obstacle_type} already registered, skipping")
            return
        
        self.obstacle_plugins[obstacle_type] = plugin
        print(f"Registered obstacle plugin: {obstacle_type}")
    
    def register_enemy_plugin(self, plugin: EnemyPlugin) -> None:
        enemy_type = plugin.get_enemy_type()
        if enemy_type in self.enemy_plugins:
            print(f"Warning: Enemy plugin {enemy_type} already registered, skipping")
            return
        
        self.enemy_plugins[enemy_type] = plugin
        print(f"Registered enemy plugin: {enemy_type}")
    
    def register_snake_modifier_plugin(self, plugin: SnakeModifierPlugin) -> None:
        modifier_type = plugin.get_modifier_type()
        if modifier_type in self.snake_modifier_plugins:
            print(f"Warning: Snake modifier plugin {modifier_type} already registered, skipping")
            return
        
        self.snake_modifier_plugins[modifier_type] = plugin
        print(f"Registered snake modifier plugin: {modifier_type}")
    
    def get_food_plugin(self, food_type: str) -> Optional[FoodPlugin]:
        return self.food_plugins.get(food_type)
    
    def get_obstacle_plugin(self, obstacle_type: str) -> Optional[ObstaclePlugin]:
        return self.obstacle_plugins.get(obstacle_type)
    
    def get_enemy_plugin(self, enemy_type: str) -> Optional[EnemyPlugin]:
        return self.enemy_plugins.get(enemy_type)
    
    def get_snake_modifier_plugin(self, modifier_type: str) -> Optional[SnakeModifierPlugin]:
        return self.snake_modifier_plugins.get(modifier_type)
    
    def get_all_food_plugins(self) -> List[FoodPlugin]:
        return list(self.food_plugins.values())
    
    def get_all_obstacle_plugins(self) -> List[ObstaclePlugin]:
        return list(self.obstacle_plugins.values())
    
    def get_all_enemy_plugins(self) -> List[EnemyPlugin]:
        return list(self.enemy_plugins.values())
    
    def get_all_snake_modifier_plugins(self) -> List[SnakeModifierPlugin]:
        return list(self.snake_modifier_plugins.values())
    
    def shutdown_all(self) -> None:
        for module in self.modules.values():
            try:
                module.shutdown()
            except Exception as e:
                print(f"Error shutting down module {module.metadata.name}: {e}")
