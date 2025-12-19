# CyberSnake Plugin System

## 概述

CyberSnake 采用基于 ECS（Entity-Component-System）架构和插件系统的设计，允许您轻松添加新的食物、障碍、敌人类型，而无需修改核心游戏代码。

## 插件结构

每个插件模块必须包含以下文件：

```
your_plugin_name/
├── your_plugin_name_main.py          # 主模块注册文件
├── your_plugin_name_food.py          # 食物插件实现
├── your_plugin_name_obstacle.py      # 障碍插件实现
├── your_plugin_name_enemy.py         # 敌人插件实现
└── your_plugin_name_snakemodify.py   # 贪吃蛇修改器实现
```

## 快速开始

### 1. 创建新插件

复制 `PLUGIN_TEMPLATE` 文件夹并重命名：

```bash
cp -r PLUGIN_TEMPLATE my_awesome_plugin
```

### 2. 重命名文件

将所有文件从 `template_*` 重命名为 `my_awesome_plugin_*`：

- `template_main.py` → `my_awesome_plugin_main.py`
- `template_food.py` → `my_awesome_plugin_food.py`
- `template_obstacle.py` → `my_awesome_plugin_obstacle.py`
- `template_enemy.py` → `my_awesome_plugin_enemy.py`
- `template_snakemodify.py` → `my_awesome_plugin_snakemodify.py`

### 3. 实现插件逻辑

根据您的需求实现各个模块。如果某个模块不需要实现（例如，您的食物不影响障碍），可以保持文件为空或只包含注释。

### 4. 注册插件

在 `my_awesome_plugin_main.py` 中的 `register_plugin` 函数中注册您的插件：

```python
def register_plugin(plugin_manager):
    from .my_awesome_plugin_food import MyFoodPlugin
    from .my_awesome_plugin_snakemodify import MySnakeModifier
    
    module = MyAwesomeModule()
    plugin_manager.register_module(module)
    
    plugin_manager.register_food_plugin(MyFoodPlugin())
    plugin_manager.register_snake_modifier_plugin(MySnakeModifier())
```

### 5. 启动游戏

插件会在游戏启动时自动被发现和加载。无需修改任何核心代码！

## 插件类型

### 食物插件 (FoodPlugin)

食物插件定义可以被贪吃蛇吃掉的物品。

**必须实现的方法：**
- `get_food_type()` - 返回食物类型的唯一标识符
- `create_food(world, position)` - 创建食物实体
- `on_food_eaten(world, event_bus, food_entity, snake_entity)` - 食物被吃掉时的处理

**可选方法：**
- `get_spawn_weight()` - 返回生成权重（默认 1.0）
- `can_spawn(world, position)` - 检查是否可以在指定位置生成

**示例：**
```python
class SpeedBoostFood(FoodPlugin):
    def get_food_type(self) -> str:
        return "speed_boost"
    
    def on_food_eaten(self, world, event_bus, food_entity, snake_entity):
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "speed_boost",
            "snake_entity": snake_entity,
            "duration": 5.0
        })
        food_entity.destroy()
```

### 障碍插件 (ObstaclePlugin)

障碍插件定义阻挡或影响贪吃蛇的物体。

**必须实现的方法：**
- `get_obstacle_type()` - 返回障碍类型的唯一标识符
- `create_obstacle(world, position)` - 创建障碍实体
- `on_collision(world, event_bus, obstacle_entity, collider_entity)` - 碰撞时的处理

**可选方法：**
- `update_obstacle(world, obstacle_entity, dt)` - 每帧更新障碍（用于移动障碍）
- `get_spawn_weight()` - 返回生成权重
- `is_deadly()` - 返回是否致命

### 敌人插件 (EnemyPlugin)

敌人插件定义具有 AI 行为的敌对实体。

**必须实现的方法：**
- `get_enemy_type()` - 返回敌人类型的唯一标识符
- `create_enemy(world, position)` - 创建敌人实体
- `update_ai(world, enemy_entity, dt)` - 更新 AI 行为
- `on_collision(world, event_bus, enemy_entity, collider_entity)` - 碰撞时的处理

**可选方法：**
- `is_boss()` - 返回是否为 Boss
- `get_spawn_weight()` - 返回生成权重
- `get_spawn_conditions()` - 返回生成条件

### 贪吃蛇修改器插件 (SnakeModifierPlugin)

修改器插件定义对贪吃蛇的各种效果。

**必须实现的方法：**
- `get_modifier_type()` - 返回修改器类型的唯一标识符
- `apply_modifier(world, event_bus, snake_entity, context)` - 应用修改器

**可选方法：**
- `can_apply(world, snake_entity)` - 检查是否可以应用
- `get_duration()` - 返回持续时间（0.0 表示永久）
- `on_modifier_end(world, snake_entity)` - 临时效果结束时调用

## 事件系统

插件可以通过事件总线与游戏系统通信：

### 常用事件

**发布事件：**
```python
event_bus.publish("event_name", {
    "key": "value"
})
```

**订阅事件：**
```python
def initialize(self, world, event_bus):
    event_bus.subscribe("food_eaten", self._on_food_eaten)

def _on_food_eaten(self, payload):
    print(f"Food eaten at {payload['position']}")
```

### 内置事件

- `food_eaten` - 食物被吃掉
- `obstacle_collision` - 碰撞障碍
- `enemy_collision` - 碰撞敌人
- `snake_self_collision` - 贪吃蛇自撞
- `apply_snake_modifier` - 应用贪吃蛇修改器
- `game_over` - 游戏结束
- `snake_grew` - 贪吃蛇增长
- `snake_shrunk` - 贪吃蛇缩短

## ECS 组件

插件可以使用以下组件：

- `PositionComponent` - 位置
- `VelocityComponent` - 速度/方向
- `BodyComponent` - 身体段（用于蛇形实体）
- `RenderComponent` - 渲染属性
- `CollisionComponent` - 碰撞属性
- `FoodComponent` - 食物属性
- `ObstacleComponent` - 障碍属性
- `EnemyComponent` - 敌人属性
- `SnakeComponent` - 贪吃蛇属性
- `AIComponent` - AI 行为
- `EffectComponent` - 临时效果
- `TimerComponent` - 计时器

## 示例插件

查看以下示例插件以了解更多：

1. **basic_food** - 基础食物（普通食物和能量食物）
2. **basic_obstacle** - 基础障碍（静态障碍）
3. **basic_enemy** - 基础敌人（随机游走的敌人）
4. **superbomb** - 超级炸弹（展示所有 4 个模块的完整示例）

## 调试

启用调试输出：

```python
def initialize(self, world, event_bus):
    print(f"[YourPlugin] Module initialized")
    event_bus.subscribe("*", self._debug_event)

def _debug_event(self, payload):
    print(f"[YourPlugin] Event: {payload}")
```

## 最佳实践

1. **模块化设计** - 每个插件应该是独立的，不依赖其他插件
2. **错误处理** - 使用 try-except 处理可能的错误
3. **性能考虑** - 避免在 update 方法中进行昂贵的计算
4. **命名规范** - 使用清晰、描述性的名称
5. **文档注释** - 为您的插件添加详细的文档字符串

## 故障排除

### 插件未加载

- 检查文件名是否正确（必须是 `pluginname_main.py`）
- 确保 `register_plugin` 函数存在
- 查看控制台输出的错误信息

### 实体不显示

- 检查 `RenderComponent` 是否正确设置
- 确认 `layer` 属性设置正确
- 验证 `visible` 属性为 `True`

### 碰撞不工作

- 确保添加了 `CollisionComponent`
- 检查 `collision_layer` 设置
- 验证位置组件是否正确更新

## 贡献

欢迎贡献新的插件！请确保：
- 代码风格一致
- 包含完整的文档
- 测试所有功能
- 遵循最佳实践

---

祝您创建出色的插件！🐍✨
