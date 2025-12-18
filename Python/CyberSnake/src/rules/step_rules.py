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
