# CyberSnake 快速开始指南

## 🎮 运行游戏

### 运行新版本（ECS + 插件系统）

```bash
python main_ecs.py
```

### 运行旧版本（兼容）

```bash
python main.py
```

## 🧪 测试插件系统

```bash
python test_plugins.py
```

## 📦 创建新插件

### 步骤 1: 复制模板

```bash
# Windows PowerShell
Copy-Item -Recurse plugins\PLUGIN_TEMPLATE plugins\my_plugin

# Linux/Mac
cp -r plugins/PLUGIN_TEMPLATE plugins/my_plugin
```

### 步骤 2: 重命名文件

将 `my_plugin` 文件夹中的所有文件从 `template_*` 重命名为 `my_plugin_*`：

- `template_main.py` → `my_plugin_main.py`
- `template_food.py` → `my_plugin_food.py`
- `template_obstacle.py` → `my_plugin_obstacle.py`
- `template_enemy.py` → `my_plugin_enemy.py`
- `template_snakemodify.py` → `my_plugin_snakemodify.py`

### 步骤 3: 实现插件

编辑 `my_plugin_main.py`：

```python
from src.plugins.plugin_interface import PluginModule, PluginMetadata

class MyPluginModule(PluginModule):
    def get_metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="MyPlugin",
            version="1.0.0",
            author="Your Name",
            description="My awesome plugin"
        )
    
    def initialize(self, world, event_bus):
        self.world = world
        self.event_bus = event_bus
        print(f"[MyPlugin] Module initialized")
    
    def shutdown(self):
        print(f"[MyPlugin] Module shutdown")

def register_plugin(plugin_manager):
    from .my_plugin_food import MyFoodPlugin
    
    module = MyPluginModule()
    plugin_manager.register_module(module)
    
    plugin_manager.register_food_plugin(MyFoodPlugin())
```

### 步骤 4: 实现食物插件

编辑 `my_plugin_food.py`：

```python
from src.plugins.plugin_interface import FoodPlugin
from src.ecs.components import (
    PositionComponent, RenderComponent, FoodComponent, CollisionComponent
)

class MyFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "my_food"
    
    def create_food(self, world, position):
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (255, 0, 0)
        render_comp.glow_color = (255, 100, 100)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "my_food"
        food_comp.score_value = 10
        entity.add_component(food_comp)
        
        entity.add_tag("food")
        return entity
    
    def on_food_eaten(self, world, event_bus, food_entity, snake_entity):
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "grow",
            "snake_entity": snake_entity,
            "amount": 2
        })
        food_entity.destroy()
```

### 步骤 5: 运行游戏

```bash
python main_ecs.py
```

你的插件会自动被加载！

## 📚 示例插件

### 查看示例

- **basic_food** - 基础食物（普通食物和能量食物）
- **basic_obstacle** - 基础障碍（静态障碍）
- **basic_enemy** - 基础敌人（随机游走）
- **superbomb** - 超级炸弹（完整示例，展示所有4个模块）

### 学习路径

1. 先看 `basic_food` 了解基本结构
2. 再看 `superbomb` 了解模块间交互
3. 参考 `PLUGIN_TEMPLATE` 创建自己的插件

## 🎯 常见任务

### 添加新食物

1. 在食物插件中实现 `FoodPlugin`
2. 在 `create_food()` 中定义外观
3. 在 `on_food_eaten()` 中定义效果

### 添加新障碍

1. 在障碍插件中实现 `ObstaclePlugin`
2. 在 `create_obstacle()` 中定义外观
3. 在 `on_collision()` 中定义碰撞效果

### 添加新敌人

1. 在敌人插件中实现 `EnemyPlugin`
2. 在 `create_enemy()` 中定义外观
3. 在 `update_ai()` 中定义AI行为
4. 在 `on_collision()` 中定义碰撞效果

### 添加贪吃蛇修改器

1. 在修改器插件中实现 `SnakeModifierPlugin`
2. 在 `apply_modifier()` 中实现效果

## 🔧 调试技巧

### 查看插件加载

运行测试脚本查看所有已加载的插件：

```bash
python test_plugins.py
```

### 启用调试输出

在插件的 `initialize()` 方法中添加：

```python
def initialize(self, world, event_bus):
    print(f"[MyPlugin] Initializing...")
    event_bus.subscribe("food_eaten", self._debug_food_eaten)

def _debug_food_eaten(self, payload):
    print(f"[MyPlugin] Food eaten: {payload}")
```

## 📖 完整文档

- `plugins/README.md` - 插件系统完整文档
- `doc/REFACTORING_SUMMARY.md` - 重构总结
- `plugins/PLUGIN_TEMPLATE/` - 插件模板（带详细注释）

## ❓ 常见问题

### Q: 插件没有被加载？

A: 检查以下几点：
1. 文件名必须是 `pluginname_main.py`
2. 必须有 `register_plugin(plugin_manager)` 函数
3. 查看控制台是否有错误信息

### Q: 实体不显示？

A: 确保：
1. 添加了 `RenderComponent`
2. 设置了正确的 `layer` 值
3. `visible` 属性为 `True`

### Q: 碰撞不工作？

A: 确保：
1. 添加了 `CollisionComponent`
2. 设置了正确的 `collision_layer`
3. 位置组件正确更新

## 🚀 进阶功能

### 使用事件系统

```python
# 发布事件
event_bus.publish("custom_event", {
    "data": "value"
})

# 订阅事件
event_bus.subscribe("custom_event", self._on_custom_event)

def _on_custom_event(self, payload):
    print(f"Received: {payload}")
```

### 查询实体

```python
# 获取所有食物实体
food_entities = world.get_entities_with_tag("food")

# 获取具有特定组件的实体
from src.ecs.components import FoodComponent, PositionComponent
entities = world.get_entities_with_components(FoodComponent, PositionComponent)
```

### 创建临时效果

```python
from src.ecs.components import EffectComponent

effect_comp = EffectComponent()
effect_comp.effect_type = "speed_boost"
effect_comp.duration = 5.0
effect_comp.intensity = 1.5
entity.add_component(effect_comp)
```

## 🎨 自定义渲染

```python
render_comp = RenderComponent()
render_comp.color = (255, 0, 0)        # 主颜色
render_comp.glow_color = (255, 100, 100)  # 发光颜色
render_comp.radius = 12                # 半径
render_comp.shape = "circle"           # 形状: "circle" 或 "square"
render_comp.layer = 2                  # 渲染层级（越大越上层）
render_comp.alpha = 255                # 透明度 (0-255)
```

## 💡 最佳实践

1. **保持模块独立** - 每个插件应该独立工作
2. **使用事件通信** - 通过事件总线与其他模块通信
3. **添加错误处理** - 使用 try-except 处理可能的错误
4. **性能优化** - 避免在 update 中进行昂贵的计算
5. **清晰命名** - 使用描述性的名称

---

祝你创建出色的插件！🐍✨
