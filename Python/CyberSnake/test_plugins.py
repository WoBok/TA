"""
测试插件系统
验证插件自动发现和注册功能
"""

from pathlib import Path
from src.ecs.world import World
from src.ecs.event_bus import EventBus
from src.plugins.plugin_manager import PluginManager

def test_plugin_system():
    print("=" * 60)
    print("CyberSnake 插件系统测试")
    print("=" * 60)
    
    # 创建ECS世界和事件总线
    world = World()
    event_bus = EventBus()
    
    # 创建插件管理器
    plugin_manager = PluginManager(world, event_bus)
    
    # 添加插件目录
    plugins_dir = Path(__file__).parent / "plugins"
    plugin_manager.add_plugin_directory(plugins_dir)
    
    print(f"\n插件目录: {plugins_dir}")
    print(f"目录存在: {plugins_dir.exists()}")
    
    # 发现并加载插件
    print("\n正在扫描插件...")
    plugin_manager.discover_plugins()
    
    # 显示加载的模块
    print(f"\n加载的模块数量: {len(plugin_manager.modules)}")
    for name, module in plugin_manager.modules.items():
        metadata = module.get_metadata()
        print(f"  - {metadata.name} v{metadata.version} by {metadata.author}")
        print(f"    {metadata.description}")
    
    # 显示食物插件
    print(f"\n食物插件数量: {len(plugin_manager.food_plugins)}")
    for food_type, plugin in plugin_manager.food_plugins.items():
        print(f"  - {food_type} (权重: {plugin.get_spawn_weight()})")
    
    # 显示障碍插件
    print(f"\n障碍插件数量: {len(plugin_manager.obstacle_plugins)}")
    for obstacle_type, plugin in plugin_manager.obstacle_plugins.items():
        print(f"  - {obstacle_type} (致命: {plugin.is_deadly()})")
    
    # 显示敌人插件
    print(f"\n敌人插件数量: {len(plugin_manager.enemy_plugins)}")
    for enemy_type, plugin in plugin_manager.enemy_plugins.items():
        print(f"  - {enemy_type} (Boss: {plugin.is_boss()})")
    
    # 显示修改器插件
    print(f"\n修改器插件数量: {len(plugin_manager.snake_modifier_plugins)}")
    for modifier_type in plugin_manager.snake_modifier_plugins.keys():
        print(f"  - {modifier_type}")
    
    # 测试创建实体
    print("\n" + "=" * 60)
    print("测试创建实体")
    print("=" * 60)
    
    # 测试创建食物
    if plugin_manager.food_plugins:
        print("\n创建食物实体...")
        for food_type, plugin in list(plugin_manager.food_plugins.items())[:2]:
            entity = plugin.create_food(world, (5, 5))
            print(f"  ✓ 创建 {food_type} 食物 (实体ID: {entity.id[:8]}...)")
    
    # 测试创建障碍
    if plugin_manager.obstacle_plugins:
        print("\n创建障碍实体...")
        for obstacle_type, plugin in list(plugin_manager.obstacle_plugins.items())[:2]:
            entity = plugin.create_obstacle(world, (10, 10))
            print(f"  ✓ 创建 {obstacle_type} 障碍 (实体ID: {entity.id[:8]}...)")
    
    # 测试创建敌人
    if plugin_manager.enemy_plugins:
        print("\n创建敌人实体...")
        for enemy_type, plugin in list(plugin_manager.enemy_plugins.items())[:2]:
            entity = plugin.create_enemy(world, (15, 15))
            print(f"  ✓ 创建 {enemy_type} 敌人 (实体ID: {entity.id[:8]}...)")
    
    # 显示世界状态
    print(f"\n世界中的实体总数: {len(world.get_all_entities())}")
    
    # 测试事件系统
    print("\n" + "=" * 60)
    print("测试事件系统")
    print("=" * 60)
    
    event_received = []
    
    def on_test_event(payload):
        event_received.append(payload)
        print(f"  ✓ 收到事件: {payload}")
    
    event_bus.subscribe("test_event", on_test_event)
    
    print("\n发布测试事件...")
    event_bus.publish("test_event", {"message": "Hello from plugin system!"})
    event_bus.process_events()
    
    if event_received:
        print(f"  ✓ 事件系统工作正常")
    else:
        print(f"  ✗ 事件系统未收到事件")
    
    # 清理
    print("\n" + "=" * 60)
    print("清理资源")
    print("=" * 60)
    
    plugin_manager.shutdown_all()
    world.clear()
    
    print("\n✓ 插件系统测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    test_plugins()
