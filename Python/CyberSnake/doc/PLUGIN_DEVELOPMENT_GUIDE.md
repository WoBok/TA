# CyberSnake 插件开发完整指南

## 目录

1. [架构概述](#架构概述)
2. [插件类型详解](#插件类型详解)
3. [开发流程](#开发流程)
4. [高级技巧](#高级技巧)
5. [实战案例](#实战案例)
6. [故障排除](#故障排除)

## 架构概述

### ECS 架构

CyberSnake 使用 Entity-Component-System (ECS) 架构：

- **Entity（实体）** - 游戏对象的容器，只有ID和组件列表
- **Component（组件）** - 纯数据，描述实体的属性
- **System（系统）** - 纯逻辑，处理具有特定组件的实体

### 事件总线

所有模块通过事件总线通信，实现解耦：

```python
# 发布事件
event_bus.publish("event_name", {"key": "value"})

# 订阅事件
event_bus.subscribe("event_name", handler_function)
```

### 插件系统

插件系统支持四种插件类型，每种插件负责不同的游戏元素：

1. **FoodPlugin** - 食物
2. **ObstaclePlugin** - 障碍
3. **EnemyPlugin** - 敌人
4. **SnakeModifierPlugin** - 贪吃蛇修改器

## 插件类型详解

### 1. FoodPlugin（食物插件）

食物插件定义可以被贪吃蛇吃掉的物品。

#### 必须实现的方法

```python
class MyFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        """返回食物类型的唯一标识符"""
        return "my_food"
    
    def create_food(self, world: World, position: Vec2) -> Entity:
        """创建食物实体"""
        entity = world.create_entity()
        
        # 添加位置组件
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        # 添加渲染组件
        render_comp = RenderComponent()
        render_comp.color = (255, 0, 0)
        render_comp.glow_color = (255, 100, 100)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        # 添加食物组件
        food_comp = FoodComponent()
        food_comp.food_type = "my_food"
        food_comp.score_value = 1
        food_comp.growth_amount = 1
        entity.add_component(food_comp)
        
        # 添加碰撞组件
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "food"
        entity.add_component(collision_comp)
        
        # 添加标签
        entity.add_tag("food")
        
        return entity
    
    def on_food_eaten(self, world: World, event_bus: EventBus, 
                      food_entity: Entity, snake_entity: Entity) -> None:
        """食物被吃掉时的处理"""
        # 应用效果
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "grow",
            "snake_entity": snake_entity,
            "amount": 1
        })
        
        # 销毁食物实体
        food_entity.destroy()
```

#### 可选方法

```python
def get_spawn_weight(self) -> float:
    """返回生成权重（默认1.0）"""
    return 5.0  # 这个食物生成概率是默认的5倍

def can_spawn(self, world: World, position: Vec2) -> bool:
    """检查是否可以在指定位置生成"""
    # 例如：只在特定条件下生成
    return len(world.get_entities_with_tag("player")) > 0
```

### 2. ObstaclePlugin（障碍插件）

障碍插件定义阻挡或影响贪吃蛇的物体。

#### 必须实现的方法

```python
class MyObstaclePlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        """返回障碍类型的唯一标识符"""
        return "my_obstacle"
    
    def create_obstacle(self, world: World, position: Vec2) -> Entity:
        """创建障碍实体"""
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (200, 0, 255)
        render_comp.glow_color = (150, 0, 200)
        render_comp.radius = 10
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        obstacle_comp = ObstacleComponent()
        obstacle_comp.obstacle_type = "my_obstacle"
        obstacle_comp.deadly = True
        obstacle_comp.movable = False
        entity.add_component(obstacle_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "obstacle"
        entity.add_component(collision_comp)
        
        entity.add_tag("obstacle")
        
        return entity
    
    def on_collision(self, world: World, event_bus: EventBus,
                    obstacle_entity: Entity, collider_entity: Entity) -> None:
        """碰撞时的处理"""
        obstacle_comp = obstacle_entity.get_component(ObstacleComponent)
        
        if obstacle_comp and obstacle_comp.deadly:
            event_bus.publish("game_over", {
                "reason": "Hit obstacle",
                "entity": collider_entity
            })
```

#### 可选方法

```python
def update_obstacle(self, world: World, obstacle_entity: Entity, dt: float) -> None:
    """每帧更新障碍（用于移动障碍）"""
    pos_comp = obstacle_entity.get_component(PositionComponent)
    if pos_comp:
        # 例如：让障碍移动
        pos_comp.x += 1

def is_deadly(self) -> bool:
    """返回是否致命"""
    return True
```

### 3. EnemyPlugin（敌人插件）

敌人插件定义具有AI行为的敌对实体。

#### 必须实现的方法

```python
class MyEnemyPlugin(EnemyPlugin):
    def get_enemy_type(self) -> str:
        """返回敌人类型的唯一标识符"""
        return "my_enemy"
    
    def create_enemy(self, world: World, position: Vec2) -> Entity:
        """创建敌人实体"""
        entity = world.create_entity()
        
        # 身体组件（蛇形敌人）
        body_comp = BodyComponent()
        body_comp.segments = [position, (position[0]-1, position[1])]
        entity.add_component(body_comp)
        
        # 速度组件
        vel_comp = VelocityComponent()
        vel_comp.direction = (1, 0)
        entity.add_component(vel_comp)
        
        # 渲染组件
        render_comp = RenderComponent()
        render_comp.color = (255, 120, 60)
        render_comp.glow_color = (255, 150, 100)
        render_comp.radius = 10
        render_comp.layer = 2
        entity.add_component(render_comp)
        
        # 敌人组件
        enemy_comp = EnemyComponent()
        enemy_comp.enemy_type = "my_enemy"
        enemy_comp.ai_behavior = "chase"
        enemy_comp.damage = 1
        entity.add_component(enemy_comp)
        
        # AI组件
        ai_comp = AIComponent()
        ai_comp.behavior = "chase"
        ai_comp.update_interval = 0.1
        entity.add_component(ai_comp)
        
        collision_comp = CollisionComponent()
        collision_comp.collision_layer = "enemy"
        entity.add_component(collision_comp)
        
        entity.add_tag("enemy")
        
        return entity
    
    def update_ai(self, world: World, enemy_entity: Entity, dt: float) -> None:
        """更新AI行为"""
        vel_comp = enemy_entity.get_component(VelocityComponent)
        body_comp = enemy_entity.get_component(BodyComponent)
        
        if not vel_comp or not body_comp:
            return
        
        # 找到玩家
        player_entities = world.get_entities_with_tag("player")
        if not player_entities:
            return
        
        player = player_entities[0]
        player_body = player.get_component(BodyComponent)
        
        if player_body:
            # 计算方向
            enemy_head = body_comp.head()
            player_head = player_body.head()
            
            dx = player_head[0] - enemy_head[0]
            dy = player_head[1] - enemy_head[1]
            
            # 选择移动方向
            if abs(dx) > abs(dy):
                vel_comp.direction = (1 if dx > 0 else -1, 0)
            else:
                vel_comp.direction = (0, 1 if dy > 0 else -1)
    
    def on_collision(self, world: World, event_bus: EventBus,
                    enemy_entity: Entity, collider_entity: Entity) -> None:
        """碰撞时的处理"""
        event_bus.publish("game_over", {
            "reason": "Hit enemy",
            "entity": collider_entity
        })
```

### 4. SnakeModifierPlugin（修改器插件）

修改器插件定义对贪吃蛇的各种效果。

#### 必须实现的方法

```python
class MySnakeModifierPlugin(SnakeModifierPlugin):
    def get_modifier_type(self) -> str:
        """返回修改器类型的唯一标识符"""
        return "my_modifier"
    
    def apply_modifier(self, world: World, event_bus: EventBus,
                      snake_entity: Entity, context: Dict[str, Any]) -> None:
        """应用修改器"""
        body_comp = snake_entity.get_component(BodyComponent)
        snake_comp = snake_entity.get_component(SnakeComponent)
        
        if not body_comp or not snake_comp:
            return
        
        # 从context获取参数
        amount = context.get("amount", 1)
        
        # 应用效果
        # 例如：增长蛇身
        # （增长通过不移除尾部实现）
        
        # 发布事件通知其他系统
        event_bus.publish("snake_modified", {
            "snake_entity": snake_entity,
            "modifier_type": self.get_modifier_type(),
            "amount": amount
        })
```

## 开发流程

### 1. 规划插件

确定你的插件需要实现哪些模块：

- 是否需要新的食物类型？
- 是否需要新的障碍类型？
- 是否需要新的敌人类型？
- 是否需要修改贪吃蛇的行为？

### 2. 创建插件目录

```bash
mkdir plugins/my_plugin
cd plugins/my_plugin
```

### 3. 创建必需文件

```
my_plugin/
├── my_plugin_main.py
├── my_plugin_food.py
├── my_plugin_obstacle.py
├── my_plugin_enemy.py
└── my_plugin_snakemodify.py
```

### 4. 实现主模块

`my_plugin_main.py`:

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
        
        # 订阅事件
        event_bus.subscribe("custom_event", self._on_custom_event)
        
        print(f"[MyPlugin] Module initialized")
    
    def _on_custom_event(self, payload):
        print(f"[MyPlugin] Custom event received: {payload}")
    
    def shutdown(self):
        print(f"[MyPlugin] Module shutdown")

def register_plugin(plugin_manager):
    # 导入插件实现
    from .my_plugin_food import MyFoodPlugin
    from .my_plugin_snakemodify import MySnakeModifier
    
    # 注册主模块
    module = MyPluginModule()
    plugin_manager.register_module(module)
    
    # 注册各类插件
    plugin_manager.register_food_plugin(MyFoodPlugin())
    plugin_manager.register_snake_modifier_plugin(MySnakeModifier())
```

### 5. 实现各个插件

根据需要实现食物、障碍、敌人和修改器插件。

### 6. 测试插件

```bash
python test_plugins.py
python main_ecs.py
```

## 高级技巧

### 模块间交互

通过事件总线实现模块间通信：

```python
# 在食物被吃时触发爆炸
def on_food_eaten(self, world, event_bus, food_entity, snake_entity):
    pos_comp = food_entity.get_component(PositionComponent)
    
    # 发布爆炸事件
    event_bus.publish("explosion", {
        "center": pos_comp.pos,
        "radius": 3,
        "source": snake_entity
    })
    
    food_entity.destroy()

# 在障碍插件中监听爆炸事件
def initialize(self, world, event_bus):
    event_bus.subscribe("explosion", self._on_explosion)

def _on_explosion(self, payload):
    center = payload["center"]
    radius = payload["radius"]
    
    # 销毁范围内的障碍
    for entity in self.world.get_entities_with_tag("obstacle"):
        pos_comp = entity.get_component(PositionComponent)
        if pos_comp:
            distance = abs(pos_comp.x - center[0]) + abs(pos_comp.y - center[1])
            if distance <= radius:
                entity.destroy()
```

### 使用定时器

```python
from src.ecs.components import TimerComponent

def create_timed_effect(self, world, snake_entity):
    timer_comp = TimerComponent()
    timer_comp.duration = 5.0
    timer_comp.callback = lambda: self._on_timer_end(snake_entity)
    snake_entity.add_component(timer_comp)

def _on_timer_end(self, snake_entity):
    print("Timer ended!")
```

### 创建临时效果

```python
from src.ecs.components import EffectComponent

effect_comp = EffectComponent()
effect_comp.effect_type = "speed_boost"
effect_comp.duration = 5.0
effect_comp.intensity = 1.5
effect_comp.data = {"original_speed": 0.12}
snake_entity.add_component(effect_comp)
```

## 实战案例

### 案例1：减速食物

创建一个食物，吃了会让贪吃蛇减速：

```python
class SlowFoodPlugin(FoodPlugin):
    def get_food_type(self) -> str:
        return "slow_food"
    
    def create_food(self, world, position):
        entity = world.create_entity()
        
        pos_comp = PositionComponent()
        pos_comp.pos = position
        entity.add_component(pos_comp)
        
        render_comp = RenderComponent()
        render_comp.color = (100, 100, 255)  # 蓝色
        render_comp.glow_color = (150, 150, 255)
        render_comp.radius = 10
        render_comp.shape = "circle"
        render_comp.layer = 1
        entity.add_component(render_comp)
        
        food_comp = FoodComponent()
        food_comp.food_type = "slow_food"
        food_comp.score_value = -1
        food_comp.effects = ["slow"]
        entity.add_component(food_comp)
        
        entity.add_tag("food")
        return entity
    
    def on_food_eaten(self, world, event_bus, food_entity, snake_entity):
        event_bus.publish("apply_snake_modifier", {
            "modifier_type": "slow",
            "snake_entity": snake_entity,
            "duration": 5.0
        })
        food_entity.destroy()
```

### 案例2：传送门障碍

创建一对传送门：

```python
class PortalObstaclePlugin(ObstaclePlugin):
    def get_obstacle_type(self) -> str:
        return "portal"
    
    def create_obstacle(self, world, position):
        # 创建传送门A
        portal_a = world.create_entity()
        pos_a = PositionComponent()
        pos_a.pos = position
        portal_a.add_component(pos_a)
        
        render_a = RenderComponent()
        render_a.color = (255, 165, 0)  # 橙色
        render_a.glow_color = (255, 200, 100)
        render_a.radius = 12
        render_a.layer = 1
        portal_a.add_component(render_a)
        
        portal_comp_a = PortalComponent()
        portal_comp_a.portal_type = "orange"
        portal_a.add_component(portal_comp_a)
        
        portal_a.add_tag("portal")
        
        return portal_a
    
    def on_collision(self, world, event_bus, obstacle_entity, collider_entity):
        portal_comp = obstacle_entity.get_component(PortalComponent)
        
        if portal_comp and portal_comp.linked_portal_id:
            # 传送到另一个传送门
            linked_portal = world.get_entity(portal_comp.linked_portal_id)
            if linked_portal:
                linked_pos = linked_portal.get_component(PositionComponent)
                collider_body = collider_entity.get_component(BodyComponent)
                
                if linked_pos and collider_body:
                    # 传送蛇头
                    collider_body.segments[0] = linked_pos.pos
```

## 故障排除

### 问题：插件未加载

**可能原因：**
1. 文件名不正确
2. 缺少 `register_plugin` 函数
3. 语法错误

**解决方法：**
```bash
python test_plugins.py
```
查看控制台输出的错误信息。

### 问题：实体不显示

**可能原因：**
1. 未添加 `RenderComponent`
2. `visible` 属性为 `False`
3. `layer` 值不正确

**解决方法：**
```python
render_comp = RenderComponent()
render_comp.visible = True
render_comp.layer = 1  # 确保在正确的层
```

### 问题：碰撞不工作

**可能原因：**
1. 未添加 `CollisionComponent`
2. `collision_layer` 不匹配
3. 位置未正确更新

**解决方法：**
确保添加碰撞组件并设置正确的层：
```python
collision_comp = CollisionComponent()
collision_comp.collision_layer = "food"  # 或 "obstacle", "enemy"
entity.add_component(collision_comp)
```

---

完整示例请参考 `plugins/superbomb/` 目录！
