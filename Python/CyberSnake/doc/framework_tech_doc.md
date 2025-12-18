# CyberSnake 技术文档（当前代码框架）

## 1. 项目目标与范围

CyberSnake 是一个基于 `pygame` 的贪吃蛇游戏项目。当前代码结构已经从“单文件脚本式实现”演进为“场景（Scene）+ 系统（System）+ 管线规则（Rules）+ 服务（Managers/Services）”的架构，以便支持：

- 多场景切换（主菜单、游戏、Game Over、各类 Overlay）
- 固定步长（Fixed-step）的确定性逻辑更新
- 可扩展的碰撞/规则处理（RulePipeline）
- 统一的 UI、事件、资源与配置服务（Services Container）

## 2. 目录结构与职责

- `main.py`
  - 项目入口，创建 `GameApp` 并启动主循环。

- `config.py`
  - 全局常量配置（屏幕尺寸、颜色、事件名、移动间隔等）。

- `src/core/`
  - **框架核心**：应用、场景抽象、场景注册。
  - `game_app.py`: `GameApp` 主循环、场景栈、服务容器。
  - `scene.py`: `Scene` 基类（事件处理、更新、绘制、生命周期钩子）。
  - `scene_registry.py`: `SceneRegistry`（scene key -> class）。

- `src/scenes/`
  - **具体场景实现**：
  - `menu_scene.py`, `game_scene.py`, `game_over_scene.py`
  - `overlay_*`: `Leaderboard/Help/Pause/Settings` 等叠加层场景
  - `scene_catalog.py`: 注册默认场景的“目录”（Catalog）
  - `scene_keys.py`: 场景 key 常量

- `src/systems/`
  - **系统层**：面向职责的逻辑模块。
  - `fixed_step_system.py`: 固定步长更新（移动、AI、碰撞规则、拾取、发事件等）。
  - `spawn_system.py`: 生成食物/道具/敌人/环境等。
  - `hud_renderer.py`: HUD/UI 绘制协助。
  - `game_tuning.py`: 从 Settings 派生运行时调参（tuning）。

- `src/rules/`
  - **规则管线层**：将“碰撞/判定/传送/死亡原因”等逻辑拆分为可组合规则。
  - `step_rules.py`: `RulePipeline`、规则注册、默认 pre/post 管线。

- `src/managers/`
  - **服务/管理器层**：为场景与系统提供通用能力。
  - `ui_manager.py`: 字体与 UI 绘制（含发光文字、界面组件等）。
  - `event_bus.py`: 简易发布订阅总线。
  - `settings.py`: `SettingsService` 读取/写入 JSON 配置并补齐默认值。
  - `resource_loader.py`: 资源路径解析（支持 PyInstaller 的 `_MEIPASS`）。
  - `input_manager.py`, `effects.py`, `leaderboard.py`: 输入、特效、榜单等。

- `src/entities/`
  - **实体层**：蛇、食物、障碍、AI、Boss、粒子、道具等。

- `src/registries/`
  - **注册表**：对可生成的 items/enemies/traps 做类型注册，并提供随机选择能力。

## 3. 启动流程（主流程）

### 3.1 入口

- 入口文件：`main.py`
  - `app = GameApp(initial_scene_cls=MenuScene)`
  - `app.run()`

### 3.2 GameApp 初始化

文件：`src/core/game_app.py`

- `pygame.init()`，创建窗口与 `clock`
- 初始化服务容器 `services`：
  - `ui`: `UIManager`
  - `events`: `EventBus`
  - `resources`: `ResourceLoader`
  - `settings`: `SettingsService`
  - `scenes`: `SceneRegistry`（由 `register_default_scenes` 填充）
- 初始化场景栈 `scene_stack`
- 注册默认事件订阅（示例：食物/能量食物事件日志输出）
- `push_scene(initial_scene_cls)` 将初始场景压栈

### 3.3 主循环（render + fixed update）

文件：`src/core/game_app.py` 的 `GameApp.run()`

主循环关键顺序：

1. 获取 `frame_dt`（基于 `clock.tick(RENDER_FPS)`）
2. `pygame.event.get()` 收集事件
3. `scene.handle_events(events)`（可能 push/pop 场景）
4. 固定步长更新：
   - 使用 `fixed_dt = 1/60` 与 `accumulator`
   - `while accumulator >= fixed_dt: scene.update_fixed(fixed_dt)`
5. 变步长更新：`scene.update(frame_dt)`（动画、过渡、非确定性更新）
6. 绘制：`scene.draw(surface)`

## 4. 场景系统（Scene Stack）

- 场景是栈结构：
  - `push_scene()`：会对当前场景调用 `on_pause()`，新场景调用 `on_enter()`
  - `pop_scene()`：弹出场景并调用 `on_exit()`，回到下一个场景会调用 `on_resume()`

- Overlay 场景（如 Leaderboard/Pause）属于“压栈叠加层”思想：
  - Overlay 可以在 `draw()` 里先绘制栈底的场景以达到“半透明叠加/暂停界面”的效果（项目中已经有类似逻辑）。

## 5. Fixed-Step 逻辑系统

文件：`src/systems/fixed_step_system.py`

- `FixedStepSystem.update_fixed(game, dt)` 是游戏逻辑的核心驱动之一。
- 逻辑上将 dt 累加到 `game.move_accum`，按 `game.step_interval_ms` 计算本次需要推进的“步数 steps”。
- 每一步中大致流程：
  - 玩家蛇推进（`snake.step(...)`）
  - pre-pipeline 规则判定（边界/传送/陷阱/障碍/自身碰撞等）
  - AI 蛇更新与食物拾取逻辑
  - post-pipeline 规则判定（AI 碰撞、幽灵猎手等）
  - 玩家拾取食物/能量食物
  - 道具拾取并 `apply(game)`
  - 触发粒子、刷光效果、事件发布（EventBus）

## 6. 规则管线（Rules / Pipeline）

文件：`src/rules/step_rules.py`

- `StepRule`: `Protocol`，规则统一接口：
  - `apply(game, player_head) -> (player_head, reason)`

- `RulePipeline.apply(...)`：顺序执行所有规则，遇到 `reason` 立刻返回。

- 规则通过 `register_step_rule(phase, priority, factory, enabled)` 注册到全局 registry。
  - `phase` 分为 `pre` / `post`
  - `priority` 用于排序
  - `factory` 返回一个 rule 实例

- 默认规则：
  - `pre`: Bounds / Portal / Trap / Obstacle / Self / BossBullet / BossBody
  - `post`: AIEnemyBody / GhostHunter

这套机制的优点是：
- 将复杂的碰撞/判定逻辑拆分成可组合单元
- 可以通过 priority 轻松调整判定顺序
- 可扩展：新增规则不必强耦合到 `FixedStepSystem`

## 7. 服务容器（Services）

`GameApp.services` 是一个轻量服务容器，为场景/系统提供共享能力。

已内置服务：
- `ui`：UI 绘制、字体资源
- `events`：EventBus
- `resources`：资源路径解析
- `settings`：JSON 配置读写
- `scenes`：SceneRegistry

使用方式（示例，见 `GameScene.__init__`）：
- `self.ui = self.app.services["ui"]`
- `self.settings = self.app.services["settings"]`

## 8. 架构潜在问题总结（风险点）

以下问题基于当前代码阅读总结，按影响优先级从高到低排序。

### 8.1 逻辑与数据模型耦合较强（game 作为“万能对象”）

- `FixedStepSystem.update_fixed(self, game, dt)` 中 `game` 形参没有显式类型约束，默认假设 `game` 拥有大量字段与方法（`snake/food/energy_food/items/events/particles/...`）。
- 风险：
  - 难以重构：字段名变动会导致运行时错误
  - 难以单元测试：需要构造一个“很完整的 game”才能测某个小逻辑

建议：
- 引入显式的 `GameContext`/`GameState` 数据类（项目已有 `src/entities/game_context.py`，可评估整合）。
- 或者为 `game` 定义 `Protocol`（静态约束）以降低隐式依赖。

### 8.2 规则注册是模块导入时执行的（隐式副作用）

- `step_rules.py` 在模块底部直接调用 `register_step_rule(...)`。
- 风险：
  - 导入顺序影响规则是否注册
  - 测试或工具脚本导入会产生副作用

建议：
- 将默认规则注册封装为显式函数，例如 `register_default_rules()`，由 `GameApp` 或 `FixedStepSystem` 初始化时调用。

### 8.3 大量 `try/except Exception: pass` 会吞掉错误

- `GameApp.push_scene/pop_scene/run` 中多处吞异常。
- `EventBus.publish` 也吞异常。
- 风险：
  - 线上体验：错误被吞后表现为“功能没反应”
  - 调试困难：难以定位真正失败原因

建议：
- 保留 fail-safe，但至少在 `settings.debug_exceptions` 时打印 traceback。
- 或统一到一个 logger（例如 `logging`）并带模块名/scene 名。

### 8.4 固定步长与“蛇移动间隔”混用，可能导致节奏不一致

- `GameApp` 有 `fixed_dt=1/60` 的固定循环；
- `FixedStepSystem` 又用 `game.step_interval_ms` 控制“每次 step”的间隔。
- 这种“双层节拍”可行，但需要小心：
  - 如果 `fixed_dt` 变化（或卡顿导致 accumulator 积压），一次会补很多 steps
  - steps 多时会在单帧内执行大量逻辑，导致卡顿尖峰

建议：
- 对 `steps` 设置上限（例如每帧最多补 N 步）以避免 spiral of death。
- 或将移动节拍完全交给 fixed_dt（例如每 tick 移动一次，速度通过 grid velocity 控制）。

### 8.5 SceneRegistry.get 未处理 key 缺失

- `SceneRegistry.get(key)` 直接 `return self._by_key[key]`。
- 风险：
  - key 拼错直接抛 `KeyError`。

建议：
- 改为抛出更明确的异常信息，或提供 `get_or_none`。

### 8.6 模块间依赖边界不清晰（跨层直接访问）

- `GameScene` 同时握有 systems、entities、managers，并在自身内调度很多逻辑。
- 风险：
  - 场景变得臃肿（God Object）

建议：
- 明确哪些是“渲染层（Scene）”、哪些是“逻辑层（Systems/Rules）”，把逻辑尽量下沉到系统/规则。

### 8.7 可测试性不足

- 当前逻辑依赖 pygame 的时间与事件（`pygame.time.get_ticks()`）。

建议：
- 对时间源做注入（TimeProvider）。
- 针对 `RulePipeline` 增加纯逻辑单测（无 pygame）。

## 9. 扩展开发指南（面向贡献者）

### 9.1 新增一个 Scene

1. 在 `src/scenes/` 新建 `xxx_scene.py` 实现 `Scene` 接口：
   - `handle_events` / `update_fixed` / `update` / `draw`
2. 在 `src/scenes/scene_keys.py` 添加 key 常量
3. 在 `src/scenes/scene_catalog.py` 的 `register_default_scenes()` 注册
4. 使用 `self.app.push_scene_key(SCENE_XXX)` 跳转

### 9.2 新增一个规则（StepRule）

1. 在 `src/rules/step_rules.py`（或拆分新文件）定义类，实现 `apply()`
2. 使用 `register_step_rule(phase=..., priority=..., factory=YourRule)` 注册
3. 通过 `priority` 控制执行顺序

### 9.3 新增可生成的道具/敌人/陷阱

- 在 `src/entities/` 新增实体
- 在对应 `src/registries/*.py` 注册
- `SpawnSystem` 里按需要调用 registry 的 `get_random_*` 生成

## 10. 术语对照

- **Scene**：界面/状态承载单元，处理输入与绘制，参与更新。
- **System**：按职责封装的逻辑模块（spawn、fixed-step、hud）。
- **Rule / Pipeline**：碰撞/判定等可组合的规则链。
- **Services**：跨场景共享的能力对象（UI、事件、资源、设置等）。

---

文档生成时间：2025-12-18
