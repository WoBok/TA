from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Protocol, Tuple

from config import GRID_WIDTH, GRID_HEIGHT


Vec2 = Tuple[int, int]


class RuleCode:
    OUT_OF_BOUNDS = "out_of_bounds"
    TRAP = "trap"
    OBSTACLE = "obstacle"
    SELF_COLLISION = "self_collision"
    BOSS_BULLET = "boss_bullet"
    BOSS_BODY = "boss_body"
    AI_BODY = "ai_body"
    HUNTER = "hunter"


@dataclass(frozen=True)
class RuleResult:
    code: str
    reason: str
    fatal: bool = True


class StepRule(Protocol):
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]: ...


class StatusEffect(Protocol):
    def is_active(self, game) -> bool: ...

    def modify_rule_result(self, game, player_head: Vec2, result: RuleResult) -> tuple[Vec2, Optional[RuleResult]]: ...


StepRuleFactory = Callable[[], StepRule]


StatusEffectFactory = Callable[[], StatusEffect]


@dataclass(frozen=True)
class StatusEffectSpec:
    priority: int
    factory: StatusEffectFactory
    enabled: bool = True


@dataclass(frozen=True)
class StepRuleSpec:
    phase: str
    priority: int
    factory: StepRuleFactory
    enabled: bool = True


@dataclass
class RulePipeline:
    rules: List[StepRule]
    status_effects: List[StatusEffectSpec]

    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        head = player_head
        for rule in self.rules:
            head, result = rule.apply(game, head)
            if not result:
                continue

            head, result = self._apply_status_effects(game, head, result)
            if result and result.fatal:
                return head, result

        return head, None

    def _apply_status_effects(
        self, game, player_head: Vec2, result: RuleResult
    ) -> tuple[Vec2, Optional[RuleResult]]:
        head = player_head
        current: Optional[RuleResult] = result
        active_specs = [s for s in self.status_effects if s.enabled]
        active_specs.sort(key=lambda s: s.priority)
        for spec in active_specs:
            if current is None:
                break
            effect = spec.factory()
            if not effect.is_active(game):
                continue
            head, current = effect.modify_rule_result(game, head, current)
        return head, current


class GhostModeStatusEffect:
    _IMMUNE_CODES = {
        RuleCode.TRAP,
        RuleCode.OBSTACLE,
        RuleCode.SELF_COLLISION,
        RuleCode.BOSS_BULLET,
        RuleCode.BOSS_BODY,
        RuleCode.AI_BODY,
        RuleCode.HUNTER,
    }

    def is_active(self, game) -> bool:
        return bool(getattr(game, "ghost_mode", False))

    def modify_rule_result(self, game, player_head: Vec2, result: RuleResult) -> tuple[Vec2, Optional[RuleResult]]:
        if result.code == RuleCode.OUT_OF_BOUNDS:
            x, y = player_head
            wrapped = (x % GRID_WIDTH, y % GRID_HEIGHT)
            game.snake.body[0] = wrapped
            return wrapped, None

        if result.code == RuleCode.BOSS_BODY:
            boss = getattr(game, "boss", None)
            if boss and not boss.is_shield_active:
                game.boss = None
                game.score += 100
            return player_head, None

        if result.code in self._IMMUNE_CODES:
            return player_head, None

        return player_head, result


@dataclass
class RuleEngine:
    _rule_registry: Dict[str, List[StepRuleSpec]]
    _status_effects: List[StatusEffectSpec]
    _defaults_registered: bool = False

    def __init__(self) -> None:
        self._rule_registry = {"pre": [], "post": []}
        self._status_effects = []
        self._defaults_registered = False

    def register_step_rule(self, *, phase: str, priority: int, factory: StepRuleFactory, enabled: bool = True) -> None:
        if phase not in self._rule_registry:
            self._rule_registry[phase] = []
        self._rule_registry[phase].append(
            StepRuleSpec(phase=phase, priority=int(priority), factory=factory, enabled=bool(enabled))
        )

    def register_status_effect(self, *, priority: int, factory: StatusEffectFactory, enabled: bool = True) -> None:
        self._status_effects.append(
            StatusEffectSpec(priority=int(priority), factory=factory, enabled=bool(enabled))
        )

    def register_default_status_effects(self) -> None:
        self.register_status_effect(priority=10, factory=GhostModeStatusEffect)

    def register_default_step_rules(self) -> None:
        self.register_step_rule(phase="pre", priority=10, factory=BoundsRule)
        self.register_step_rule(phase="pre", priority=20, factory=PortalTeleportRule)
        self.register_step_rule(phase="pre", priority=30, factory=TrapCollisionRule)
        self.register_step_rule(phase="pre", priority=40, factory=ObstacleCollisionRule)
        self.register_step_rule(phase="pre", priority=50, factory=SelfCollisionRule)
        self.register_step_rule(phase="pre", priority=60, factory=BossBulletCollisionRule)
        self.register_step_rule(phase="pre", priority=70, factory=BossBodyCollisionRule)

        self.register_step_rule(phase="post", priority=10, factory=AIEnemyBodyCollisionRule)
        self.register_step_rule(phase="post", priority=20, factory=GhostHunterCollisionRule)

    def ensure_defaults_registered(self) -> None:
        if self._defaults_registered:
            return
        self.register_default_status_effects()
        self.register_default_step_rules()
        self._defaults_registered = True

    def build_pipeline(self, phase: str) -> RulePipeline:
        self.ensure_defaults_registered()
        specs = [s for s in self._rule_registry.get(phase, []) if s.enabled]
        specs.sort(key=lambda s: s.priority)
        status_specs = [s for s in self._status_effects if s.enabled]
        return RulePipeline(rules=[s.factory() for s in specs], status_effects=status_specs)


DEFAULT_RULE_ENGINE = RuleEngine()


def create_default_rule_engine() -> RuleEngine:
    engine = RuleEngine()
    engine.ensure_defaults_registered()
    return engine


def register_step_rule(*, phase: str, priority: int, factory: StepRuleFactory, enabled: bool = True) -> None:
    DEFAULT_RULE_ENGINE.register_step_rule(phase=phase, priority=priority, factory=factory, enabled=enabled)


def register_status_effect(*, priority: int, factory: StatusEffectFactory, enabled: bool = True) -> None:
    DEFAULT_RULE_ENGINE.register_status_effect(priority=priority, factory=factory, enabled=enabled)


def ensure_default_registrations() -> None:
    DEFAULT_RULE_ENGINE.ensure_defaults_registered()


def build_default_pre_enemy_pipeline() -> RulePipeline:
    return DEFAULT_RULE_ENGINE.build_pipeline("pre")


def build_default_post_enemy_pipeline() -> RulePipeline:
    return DEFAULT_RULE_ENGINE.build_pipeline("post")


class BoundsRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        x, y = player_head
        if 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT:
            return player_head, None

        return player_head, RuleResult(code=RuleCode.OUT_OF_BOUNDS, reason="撞到边界了！")


class PortalTeleportRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        if not game.portals:
            return player_head, None

        teleported = game.portals.teleport(player_head)
        if teleported != player_head:
            game.snake.body[0] = teleported
            return teleported, None

        return player_head, None


class TrapCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        for trap in game.traps:
            if trap.is_active() and player_head == trap.pos:
                return player_head, RuleResult(code=RuleCode.TRAP, reason="掉进了陷阱！")

        return player_head, None


class ObstacleCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        if player_head in game.obstacles.cells:
            return player_head, RuleResult(code=RuleCode.OBSTACLE, reason="撞到荆棘了！")

        return player_head, None


class SelfCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        if player_head in game.snake.body[1:]:
            return player_head, RuleResult(code=RuleCode.SELF_COLLISION, reason="撞到自己了！")

        return player_head, None


class BossBulletCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        if not game.boss:
            return player_head, None

        for bullet in game.boss.bullets:
            if bullet.get_grid_pos() == player_head:
                return player_head, RuleResult(code=RuleCode.BOSS_BULLET, reason="被Boss子弹击中！")

        return player_head, None


class BossBodyCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        if not game.boss:
            return player_head, None

        if player_head not in game.boss.get_body_cells():
            return player_head, None

        return player_head, RuleResult(code=RuleCode.BOSS_BODY, reason="撞到了Boss！")


class GhostHunterCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        for hunter in game.ghost_hunters:
            if hunter.visible and hunter.get_grid_pos() == player_head:
                return player_head, RuleResult(code=RuleCode.HUNTER, reason="被幽灵猎手抓住了！")

        return player_head, None


class AIEnemyBodyCollisionRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        for ai in game.ai_snakes:
            if player_head in ai.body:
                return player_head, RuleResult(code=RuleCode.AI_BODY, reason="被AI蛇撞到了！")

        return player_head, None


class ExampleCustomFailRule:
    def apply(self, game, player_head: Vec2) -> tuple[Vec2, Optional[RuleResult]]:
        return player_head, None
