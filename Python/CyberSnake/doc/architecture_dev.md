# CyberSnake 代码架构开发文档

本文档面向后续开发与维护，描述当前工程的架构设计、扩展点、模块依赖关系，以及主要耦合风险。

## 1. 目录结构与分层

项目采用“入口层 -> 核心框架层 -> 场景层 -> 实体/系统层 -> 管理器层 -> 注册表层”的组织方式。

- `main.py`
  - 程序入口，仅负责创建 `GameApp` 并指定初始场景。
- `config.py`
  - 全局常量与配置（窗口尺寸、颜色、节奏、事件名常量等）。
- `src/core/`
  - 游戏运行框架（主循环、Scene 基类、Scene 注册中心）。
- `src/scenes/`
  - 以“场景/界面”为单位组织游戏流程（Menu/Game/GameOver/Overlay 等）。
- `src/entities/`
  - 纯实体/对象（蛇、食物、障碍、Boss、敌人、粒子、道具、陷阱等）。
- `src/managers/`
  - 运行期服务/系统（UI、事件总线、设置、资源加载、输入、效果）。
- `src/registries/`
  - “可插拔内容”注册表（道具/陷阱/敌人等），负责统一随机选择与启用控制。

## 2. 程序启动与运行主循环

启动入口：

- `main.py` -> `GameApp(initial_scene_cls=MenuScene)` -> `GameApp.run()`

核心主循环在 `src/core/game_app.py`：

- 初始化 `pygame`、窗口、时钟。
- 初始化 `services`（服务容器）。
- 初始化 `SceneRegistry`（场景注册中心）并注册默认场景。
- 使用 Scene 栈（`scene_stack`）管理“当前场景 + Overlay”。
- 游戏循环每帧执行：
  - 收集 `pygame.event.get()`
  - `current_scene.handle_events(events)`
  - 固定步长逻辑：`current_scene.update_fixed(fixed_dt)`（可能执行多次，保持确定性）
  - 变步长逻辑：`current_scene.update(frame_dt)`（动画/特效/计时器更适合放这里）
  - 渲染：`current_scene.draw(screen)` + `pygame.display.flip()`

### 2.1 固定步长与变步长的设计意图

- `update_fixed(dt)`
  - 推荐放“网格移动、碰撞、得分等确定性规则”，减少不同机器帧率差异。
- `update(dt)`
  - 推荐放“粒子、刷光、UI 动画、Boss 子弹插值”等视觉或非确定性逻辑。

## 3. Scene 与 Scene 栈

### 3.1 Scene 基类

`src/core/scene.py` 定义场景生命周期与接口：

- `handle_events(events)`
- `update_fixed(dt)`（默认空实现）
- `update(dt)`
- `draw(surface)`

### 3.2 Scene 栈（Overlay）

`GameApp` 使用 Scene 栈实现 Overlay：

- `push_scene(scene_cls)`：压栈并进入场景，同时给旧场景 `on_pause()`
- `pop_scene()`：弹栈并恢复下层场景 `on_resume()`

Overlay 场景（例如暂停、排行榜、设置、帮助）通常会：

- 绘制时先绘制下层场景，再叠加半透明遮罩。
- 事件处理只处理“关闭/切换”的按键。

### 3.3 SceneRegistry：减少跨 Scene 强耦合

为降低场景之间的直接 `import` 耦合，项目引入：

- `src/core/scene_registry.py`：`SceneRegistry`（key -> SceneClass）
- `src/scenes/scene_keys.py`：集中定义 key
- `src/scenes/scene_catalog.py`：集中注册默认 Scene

在 `GameApp` 中新增：

- `push_scene_key(scene_key)`：通过 key 推入场景

效果：

- 新增 UI 界面时，主要改动集中在 `scene_keys.py + scene_catalog.py`，业务场景只需调用 `push_scene_key()`。
- 降低“场景之间互相 import”导致的循环依赖与耦合。

## 4. Services 服务容器

`GameApp.services` 是一个轻量服务容器，场景通过 `self.app.services[...]` 获取公共服务。

当前包含：

- `ui`：`UIManager`，负责发光文字等 UI 绘制封装。
- `events`：`EventBus`，发布/订阅事件，减少模块直接依赖。
- `resources`：`ResourceLoader`，统一处理资源路径（兼容 PyInstaller）。
- `settings`：`SettingsService`，本地 JSON 设置读写（show_fps/log_events）。
- `scenes`：`SceneRegistry`，场景 key 路由。

这种设计的扩展方式：

- 未来增加音效、存档、成就等系统，只需在 `services` 中新增一项服务，并在相关模块中按需使用。

## 5. EventBus 事件中心（解耦用）

位置：`src/managers/event_bus.py`

- 订阅：`bus.subscribe(event_type, handler)`
- 发布：`bus.publish(event_type, payload)`

事件名集中于 `config.py`：

- `EVT_FOOD_EATEN`
- `EVT_ENERGY_EATEN`

当前用法：

- `GameScene` 在吃到食物时发布事件。
- `GameApp` 订阅事件（受 `settings.log_events` 控制）进行日志输出。

扩展建议：

- UI（例如浮动提示、成就弹窗）、音效系统、数据统计系统都可以订阅同一事件，而不与 `GameScene` 直接耦合。

## 6. Registry（道具/陷阱/敌人）与内容扩展

### 6.1 通用 Registry

位置：`src/registries/registry.py`

- `register(value, weight=1, tags=...)`
- `choose_random(require_tags=...)`
- 规则：`weight=0` 表示“注册但默认禁用”（不会被随机选中）。

### 6.2 Items / Traps / Enemies

- `src/registries/items.py`
  - `get_random_item()` 返回一个道具类（默认均匀随机）。
  - 示例：`ScoreBoost` 已注册为 `weight=0`。
- `src/registries/traps.py`
  - `get_random_trap()` 返回陷阱类。
- `src/registries/enemies.py`
  - `get_random_enemy()` 返回敌人类。
  - 敌人使用 `AIEnemy` 协议（`src/entities/enemy_types.py`）。
  - 示例敌人 `WanderingAISnake` 已注册为 `weight=0`。

### 6.3 扩展方式（推荐流程）

新增一个道具：

1. 在 `src/entities/items.py` 新增一个 `Item` 子类，实现 `apply(game)`。
2. 在 `src/registries/items.py` 注册：`ITEM_REGISTRY.register(NewItem, weight=1)`。

新增一个敌人：

1. 新增一个满足 `AIEnemy` 协议的类（有 `body/update_ai/step/draw`）。
2. 在 `src/registries/enemies.py` 注册：`ENEMY_REGISTRY.register(NewEnemy, weight=1)`。

新增一个 UI 界面：

1. 在 `src/scenes/` 新建 Scene 类。
2. 在 `scene_keys.py` 增加 key。
3. 在 `scene_catalog.py` 注册 key -> Scene。
4. 业务场景使用 `app.push_scene_key(key)`。

## 7. 模块耦合度评估

下面以“依赖方向是否单向、是否依赖具体实现、是否存在循环依赖风险”为衡量标准。

### 7.1 低耦合（良好）

- `main.py` -> `GameApp`：入口清晰。
- `Scene` 通过 `services` 获取依赖：减少全局 import。
- `EventBus`：通过事件解耦（发布者不需要知道订阅者是谁）。
- `SceneRegistry`：通过 key 解耦场景之间的直接依赖。
- `Registry`：道具/陷阱/敌人扩展只需注册，不需要改 `GameScene` 的生成结构。

### 7.2 中耦合（可接受，但未来可能需要继续拆分）

- `GameScene` 聚合了大量玩法系统（生成、碰撞、计分、Boss、渲染、HUD）。
  - 这是典型的“场景上帝类”风险点。
  - 目前规模可控，但后期再增加多种敌人/道具/关卡规则时，建议拆成多个 system（如 SpawnSystem/CollisionSystem/RenderSystem）。

### 7.3 高耦合（需要留意）

- 道具 `Item.apply(game)` 直接操作 `GameScene` 的内部字段（例如 `game.score`、`game.obstacles`）。
  - 优点：实现快速。
  - 风险：随着内容变多，`GameScene` 会被迫暴露越来越多内部结构。
  - 演进方向：可引入“GameContext/接口层”，让道具只依赖更稳定的 API。

## 8. 设计与防御性建议（不改变现有玩法的前提）

- 建议逐步减少“捕获异常后静默忽略”的写法，至少在 `log_events` 或 debug 模式下输出 traceback，便于定位问题。
- 进一步数据驱动：将 `GameScene` 内部的掉落间隔、连击窗口等数值提取为 `dataclass` 配置对象，并允许从 JSON 覆盖。
- 将 `GameScene` 拆分为多个 system 以降低维护成本（当内容继续增长时再做，避免早期过度工程化）。

## 9. 快速自检清单

- 新增 Scene 后：
  - 是否在 `scene_keys.py` 添加 key
  - 是否在 `scene_catalog.py` 注册
  - 是否通过 `push_scene_key()` 进入
- 新增道具/敌人/陷阱后：
  - 是否注册到对应 registry
  - 默认是否设置 `weight=0` 以免影响现有玩法

