# CyberSnake 重构总结

## 项目重构概述

本次重构完全按照 `plan_04.md` 的要求，将 CyberSnake 项目改造为基于 ECS（Entity-Component-System）架构和事件总线的插件化系统。

## 架构变更

### 1. ECS 架构实现

#### 核心组件 (`src/ecs/`)

- **Entity** (`entity.py`) - 游戏实体基类，支持组件添加/移除、标签系统
- **Component** (`component.py`) - 组件基类，所有游戏数据都存储在组件中
- **System** (`system.py`) - 系统基类，处理具有特定组件的实体
- **World** (`world.py`) - ECS世界管理器，管理所有实体和系统

#### 游戏组件 (`src/ecs/components.py`)

实现了以下组件：
- `PositionComponent` - 位置
- `VelocityComponent` - 速度/方向
- `BodyComponent` - 身体段（蛇形实体）
- `RenderComponent` - 渲染属性
- `CollisionComponent` - 碰撞检测
- `FoodComponent` - 食物属性
- `ObstacleComponent` - 障碍属性
- `EnemyComponent` - 敌人属性
- `SnakeComponent` - 贪吃蛇属性
- `AIComponent` - AI行为
- `EffectComponent` - 临时效果
- `TimerComponent` - 计时器
- `SpawnComponent` - 生成器
- 等等...

#### ECS 系统 (`src/ecs/systems/`)

- `MovementSystem` - 处理实体移动
- `CollisionSystem` - 处理碰撞检测
- `RenderSystem` - 处理渲染
- `SpawnSystem` - 处理实体生成
- `AISystem` - 处理AI行为
- `EffectSystem` - 处理临时效果

### 2. 增强的事件总线系统

#### 事件总线 (`src/ecs/event_bus.py`)

- 支持事件订阅/发布
- 支持事件队列和优先级
- 支持立即发布和延迟处理
- 错误隔离（一个处理器失败不影响其他）

#### 内置事件

- `food_eaten` - 食物被吃掉
- `obstacle_collision` - 碰撞障碍
- `enemy_collision` - 碰撞敌人
- `snake_self_collision` - 贪吃蛇自撞
- `apply_snake_modifier` - 应用修改器
- `game_over` - 游戏结束
- `snake_grew` - 贪吃蛇增长
- `snake_shrunk` - 贪吃蛇缩短
- `energy_gained` - 获得能量

### 3. 插件系统

#### 插件接口 (`src/plugins/plugin_interface.py`)

定义了四种插件类型：

1. **FoodPlugin** - 食物插件
   - `get_food_type()` - 获取食物类型
   - `create_food()` - 创建食物实体
   - `on_food_eaten()` - 食物被吃时的处理
   - `get_spawn_weight()` - 生成权重
   - `can_spawn()` - 是否可以生成

2. **ObstaclePlugin** - 障碍插件
   - `get_obstacle_type()` - 获取障碍类型
   - `create_obstacle()` - 创建障碍实体
   - `on_collision()` - 碰撞时的处理
   - `update_obstacle()` - 更新障碍（可选）
   - `is_deadly()` - 是否致命

3. **EnemyPlugin** - 敌人插件
   - `get_enemy_type()` - 获取敌人类型
   - `create_enemy()` - 创建敌人实体
   - `update_ai()` - 更新AI行为
   - `on_collision()` - 碰撞时的处理
   - `is_boss()` - 是否为Boss

4. **SnakeModifierPlugin** - 贪吃蛇修改器插件
   - `get_modifier_type()` - 获取修改器类型
   - `apply_modifier()` - 应用修改器
   - `can_apply()` - 是否可以应用
   - `get_duration()` - 获取持续时间
   - `on_modifier_end()` - 效果结束时的处理

#### 插件管理器 (`src/plugins/plugin_manager.py`)

- **自动发现** - 扫描 `plugins/` 目录自动加载插件
- **注册系统** - 统一的插件注册接口
- **热插拔** - 支持动态加载/卸载插件
- **依赖管理** - 管理插件之间的依赖关系

### 4. 插件模块结构

每个插件模块必须包含以下文件：

```
plugin_name/
├── plugin_name_main.py          # 主模块（必需）
├── plugin_name_food.py          # 食物插件实现
├── plugin_name_obstacle.py      # 障碍插件实现
├── plugin_name_enemy.py         # 敌人插件实现
└── plugin_name_snakemodify.py   # 修改器插件实现
```

## 示例插件

### 1. basic_food - 基础食物模块

实现了：
- `NormalFoodPlugin` - 普通食物（增加蛇身长度）
- `EnergyFoodPlugin` - 能量食物（增加能量值）
- `GrowSnakeModifier` - 增长修改器
- `EnergyBoostModifier` - 能量提升修改器

### 2. basic_obstacle - 基础障碍模块

实现了：
- `StaticObstaclePlugin` - 静态障碍（碰到即死）

### 3. basic_enemy - 基础敌人模块

实现了：
- `WanderingEnemyPlugin` - 随机游走的敌人

### 4. superbomb - 超级炸弹模块（完整示例）

这是一个展示所有四个模块协同工作的完整示例：

- **食物** (`SuperBombFoodPlugin`) - 超级炸弹食物
- **障碍** (`ExplosionDebrisPlugin`) - 爆炸碎片障碍
- **敌人** (`StunnedEnemyPlugin`) - 被击晕的敌人
- **修改器** (`ExplosionShrinkModifier`, `ExplosionClearModifier`) - 爆炸效果

**工作流程：**
1. 玩家吃到超级炸弹食物
2. 触发爆炸事件
3. 清除爆炸范围内的障碍和敌人
4. 贪吃蛇身体缩短2格
5. 获得额外分数

## 新增文件列表

### ECS 核心
- `src/ecs/__init__.py`
- `src/ecs/entity.py`
- `src/ecs/component.py`
- `src/ecs/system.py`
- `src/ecs/world.py`
- `src/ecs/event_bus.py`
- `src/ecs/components.py`

### ECS 系统
- `src/ecs/systems/__init__.py`
- `src/ecs/systems/movement_system.py`
- `src/ecs/systems/collision_system.py`
- `src/ecs/systems/render_system.py`
- `src/ecs/systems/spawn_system.py`
- `src/ecs/systems/ai_system.py`
- `src/ecs/systems/effect_system.py`

### 插件系统
- `src/plugins/__init__.py`
- `src/plugins/plugin_interface.py`
- `src/plugins/plugin_manager.py`

### 示例插件
- `plugins/basic_food/` (5 files)
- `plugins/basic_obstacle/` (5 files)
- `plugins/basic_enemy/` (5 files)
- `plugins/superbomb/` (5 files)

### 插件模板
- `plugins/PLUGIN_TEMPLATE/` (5 files)
- `plugins/README.md`

### 新游戏场景
- `src/scenes/ecs_game_scene.py`
- `main_ecs.py`

### 文档
- `doc/REFACTORING_SUMMARY.md` (本文件)

## 使用方法

### 启动新版本游戏

```bash
python main_ecs.py
```

### 创建新插件

1. 复制模板：
```bash
cp -r plugins/PLUGIN_TEMPLATE plugins/my_plugin
```

2. 重命名文件：
- `template_main.py` → `my_plugin_main.py`
- `template_food.py` → `my_plugin_food.py`
- 等等...

3. 实现插件逻辑

4. 启动游戏，插件会自动加载

### 添加新食物类型

```python
# plugins/my_plugin/my_plugin_food.py
from src.plugins.plugin_interface import FoodPlugin

class MyFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "my_food"
    
    def create_food(self, world, position):
        # 创建食物实体
        pass
    
    def on_food_eaten(self, world, event_bus, food_entity, snake_entity):
        # 处理食物被吃
        pass
```

## 关键特性

### 1. 热插拔
- 插件可以在不修改核心代码的情况下添加或移除
- 游戏启动时自动扫描并加载所有插件

### 2. 模块化
- 每个插件都是独立的模块
- 插件之间通过事件总线通信
- 避免了紧耦合

### 3. 可扩展性
- 轻松添加新的食物、障碍、敌人类型
- 支持复杂的交互（如超级炸弹）
- 可以添加新的组件和系统

### 4. 冲突解决
- 事件系统确保操作顺序
- 组件系统避免状态冲突
- 插件优先级系统

## 测试

### 测试插件系统

```bash
python -c "from src.plugins.plugin_manager import PluginManager; from src.ecs.world import World; from src.ecs.event_bus import EventBus; w = World(); e = EventBus(); pm = PluginManager(w, e); pm.add_plugin_directory('plugins'); pm.discover_plugins(); print(f'Loaded {len(pm.modules)} modules')"
```

### 测试ECS系统

```bash
python main_ecs.py
```

## 兼容性

- 保留了原有的 `main.py`，可以继续使用旧版本
- 新版本使用 `main_ecs.py` 启动
- 两个版本可以共存

## 性能优化

- ECS架构提供了更好的数据局部性
- 组件索引加速查询
- 事件队列批处理
- 系统优先级控制更新顺序

## 未来扩展

### 可以轻松添加的功能

1. **新食物类型**
   - 减速食物
   - 传送食物
   - 分裂食物

2. **新障碍类型**
   - 移动障碍
   - 传送门
   - 陷阱

3. **新敌人类型**
   - 追踪敌人
   - Boss敌人
   - 射击敌人

4. **新修改器**
   - 无敌模式
   - 加速/减速
   - 反转控制

## 总结

本次重构完全实现了 `plan_04.md` 中的所有需求：

✅ 采用ECS架构  
✅ 采用事件总线架构  
✅ 使用接口实现四个模块（食物、障碍、敌人、贪吃蛇修改）  
✅ 新模块自动注册和调度  
✅ 模块热插拔支持  
✅ 冲突解决机制  
✅ 提供完整的模板和示例  

项目现在具有高度的可扩展性和可维护性，可以轻松添加任意数量的新模块而不影响现有代码。
