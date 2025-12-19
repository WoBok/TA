from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Protocol, Tuple

from config import GRID_WIDTH, GRID_HEIGHT


Vec2 = Tuple[int, int]


class StepRule(Protocol):
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]: ...


StepRuleFactory = Callable[[], StepRule]


@dataclass(frozen=True)
class StepRuleSpec:
    phase: str
    priority: int
    factory: StepRuleFactory
    enabled: bool = True


@dataclass
class RulePipeline:
    rules: List[StepRule]

    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        head = player_head
        for rule in self.rules:
            head, reason = rule.apply(game, head)
            if reason:
                return head, reason
        return head, None


_RULE_REGISTRY: Dict[str, List[StepRuleSpec]] = {"pre": [], "post": []}


def register_step_rule(*, phase: str, priority: int, factory: StepRuleFactory, enabled: bool = True) -> None:
    if phase not in _RULE_REGISTRY:
        _RULE_REGISTRY[phase] = []
    _RULE_REGISTRY[phase].append(StepRuleSpec(phase=phase, priority=int(priority), factory=factory, enabled=bool(enabled)))


def _build_pipeline_for_phase(phase: str) -> RulePipeline:
    specs = [s for s in _RULE_REGISTRY.get(phase, []) if s.enabled]
    specs.sort(key=lambda s: s.priority)
    return RulePipeline(rules=[s.factory() for s in specs])


class BoundsRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        x, y = player_head
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return player_head, None

        if game.ghost_mode:
            wrapped = (x % GRID_WIDTH, y % GRID_HEIGHT)
            game.snake.body[0] = wrapped
            return wrapped, None

        return player_head, "撞到边界了！"


class PortalTeleportRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if not game.portals:
            return player_head, None

        teleported = game.portals.teleport(player_head)
        if teleported != player_head:
            game.snake.body[0] = teleported
            return teleported, None

        return player_head, None


class TrapCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if game.ghost_mode:
            return player_head, None

        for trap in game.traps:
            if trap.is_active() and player_head == trap.pos:
                return player_head, "掉进了陷阱！"

        return player_head, None


class ObstacleCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if game.ghost_mode:
            return player_head, None

        if player_head in game.obstacles.cells:
            return player_head, "撞到荆棘了！"

        return player_head, None


class SelfCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if game.ghost_mode:
            return player_head, None

        if player_head in game.snake.body[1:]:
            return player_head, "撞到自己了！"

        return player_head, None


class BossBulletCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if not game.boss or game.ghost_mode:
            return player_head, None

        for bullet in game.boss.bullets:
            if bullet.get_grid_pos() == player_head:
                return player_head, "被Boss子弹击中！"

        return player_head, None


class BossBodyCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if not game.boss:
            return player_head, None

        if player_head not in game.boss.get_body_cells():
            return player_head, None

        if game.ghost_mode and not game.boss.is_shield_active:
            game.boss = None
            game.score += 100
            return player_head, None

        if not game.ghost_mode:
            return player_head, "撞到了Boss！"

        return player_head, None


class GhostHunterCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if game.ghost_mode:
            return player_head, None

        for hunter in game.ghost_hunters:
            if hunter.visible and hunter.get_grid_pos() == player_head:
                return player_head, "被幽灵猎手抓住了！"

        return player_head, None


class AIEnemyBodyCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        if game.ghost_mode:
            return player_head, None

        for ai in game.ai_snakes:
            if player_head in ai.body:
                return player_head, "被AI蛇撞到了！"

        return player_head, None


class ExampleCustomFailRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        return player_head, None


def build_default_pre_enemy_pipeline() -> RulePipeline:
    return _build_pipeline_for_phase("pre")


def build_default_post_enemy_pipeline() -> RulePipeline:
    return _build_pipeline_for_phase("post")


register_step_rule(phase="pre", priority=10, factory=BoundsRule)
register_step_rule(phase="pre", priority=20, factory=PortalTeleportRule)
register_step_rule(phase="pre", priority=30, factory=TrapCollisionRule)
register_step_rule(phase="pre", priority=40, factory=ObstacleCollisionRule)
register_step_rule(phase="pre", priority=50, factory=SelfCollisionRule)
register_step_rule(phase="pre", priority=60, factory=BossBulletCollisionRule)
register_step_rule(phase="pre", priority=70, factory=BossBodyCollisionRule)

register_step_rule(phase="post", priority=10, factory=AIEnemyBodyCollisionRule)
register_step_rule(phase="post", priority=20, factory=GhostHunterCollisionRule)
这些是我游戏结束的出发条件管线，会在主循环中不断地检测，你觉得这样做好吗？或者还有什么更好的方法吗

---
---

这种基于**规则管线（Rule Pipeline）**的设计在代码结构上非常优雅，特别是在处理复杂的“贪吃蛇”变体（包含传送门、Boss、AI敌人等）时，它的扩展性比冗长的 `if-else` 嵌套要好得多。

不过，从**性能优化**和**逻辑严密性**的角度来看，目前的实现方式在“主循环不断检测”的情况下存在一些潜在问题。以下是我的分析和改进建议：

---

### 1. 现状优点

* **解耦性强**：每个规则（Rule）都是独立的类，增删功能只需在注册处修改。
* **优先级可控**：通过 `priority` 明确了检测顺序（例如：应该先算传送，再算碰撞）。
* **配置化**：`_RULE_REGISTRY` 允许你动态地开启或关闭某些规则。

### 2. 存在的潜在问题

* **重复分配对象（性能）**：在 `_build_pipeline_for_phase` 中，你每次调用都会执行 `[s.factory() for s in specs]`。这意味着**每一帧**你都在实例化大量的规则对象。虽然 Python 的 GC 很强，但在高频游戏循环中这是不必要的开销。
* **逻辑链条的副作用**：`PortalTeleportRule` 直接修改了 `game.snake.body[0]`。如果后面的规则判定玩家死亡，此时蛇头位置已经改变，可能会导致渲染一帧“蛇头进入墙内后才死”的违和感。
* **缺少“位置预测”**：目前是“发生了碰撞才处理”。在某些高速移动或物理模拟中，通常建议“预测下一帧位置”，如果下一帧会撞，则本帧停止移动。

---

### 3. 更好的改进方案

#### A. 静态构建管线（单例化）

不要在循环中不断 `build` 管线。管线应该在游戏初始化或关卡加载时构建一次，之后重复使用。

```python
# 修改规则类为无状态或单例
class RulePipeline:
    def __init__(self, rules: List[StepRule]):
        self.rules = rules

    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[str]]:
        current_head = player_head
        for rule in self.rules:
            # 传入当前的 head，让规则决定是否移动或报错
            current_head, reason = rule.apply(game, current_head)
            if reason:
                return current_head, reason
        return current_head, None

# 全局缓存构建好的管线
_PIPELINE_CACHE: Dict[str, RulePipeline] = {}

def get_pipeline(phase: str) -> RulePipeline:
    if phase not in _PIPELINE_CACHE:
        _PIPELINE_CACHE[phase] = _build_pipeline_for_phase(phase)
    return _PIPELINE_CACHE[phase]

```

#### B. 引入 "碰撞预测" 逻辑

现在的 `apply` 会直接修改 `game.snake.body[0]`。建议改为**纯函数式**处理：

1. 传入“意图移动的位置”。
2. 规则链返回“实际落脚点”和“状态”。
3. 只有当没有任何规则导致死亡时，主逻辑才更新蛇的位置。

#### C. 空间分区优化（针对 AI 和 障碍物）

如果你有大量的 AI 蛇或障碍物，目前的 `for ai in game.ai_snakes` 是  复杂度。

* **改进**：使用一个全局的 `CollisionMap`（二维数组或 Hash Set），每帧更新一次 AI 的位置到 Map 中。规则检测只需  查询 Map 即可。

---

### 4. 推荐的架构示意图

为了更清晰地展示逻辑流，你可以参考以下管线处理流程：

### 5. 扩展建议：事件驱动

如果你的游戏变复杂，可以引入**事件总线（Event Bus）**。
例如：`BossBodyCollisionRule` 不直接返回字符串，而是抛出一个 `PlayerDeathEvent`。这样你可以让 UI 模块、音效模块分别监听这个事件，实现“撞击瞬间屏幕抖动+播放死亡音效+弹出菜单”的联动，而不需要把这些逻辑都写在 Rule 类里。

### 总结

你现在的写法**已经优于 90% 的初学者**。
**下一步动作：**

1. **缓存管线对象**，避免每一帧都 `new` 新对象。
2. **分离“位置计算”与“属性修改”**，确保在确认存活前不要修改蛇的实际数据。
3. **统一提示语**：考虑将硬编码的中文字符串（如 "撞到边界了！"）放入专门的语言包或常量类中。

你想让我帮你重构一下 `RulePipeline` 的构建部分以提升性能吗？