from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterable, List, Optional, Sequence, Set, TypeVar
import random

T = TypeVar("T")


@dataclass(frozen=True)
class RegistryEntry(Generic[T]):
    value: T
    weight: int = 1
    tags: Set[str] = field(default_factory=set)


class Registry(Generic[T]):
    def __init__(self) -> None:
        self._entries: List[RegistryEntry[T]] = []

    def register(self, value: T, *, weight: int = 1, tags: Optional[Iterable[str]] = None) -> None:
        tag_set = set(tags) if tags else set()
        entry = RegistryEntry(value=value, weight=max(0, int(weight)), tags=tag_set)
        self._entries.append(entry)

    def entries(self) -> Sequence[RegistryEntry[T]]:
        return tuple(self._entries)

    def choose_random(self, *, require_tags: Optional[Iterable[str]] = None) -> T:
        if not self._entries:
            raise ValueError("registry is empty")

        req = set(require_tags) if require_tags else None
        candidates: List[RegistryEntry[T]]
        if req:
            candidates = [e for e in self._entries if req.issubset(e.tags)]
        else:
            candidates = list(self._entries)

        if not candidates:
            raise ValueError("no registry entries match tag constraints")

        candidates = [e for e in candidates if e.weight > 0]
        if not candidates:
            raise ValueError("no enabled registry entries match tag constraints")

        weights = [e.weight for e in candidates]
        if all(w == 1 for w in weights):
            return random.choice(candidates).value
        return random.choices([e.value for e in candidates], weights=weights, k=1)[0]
