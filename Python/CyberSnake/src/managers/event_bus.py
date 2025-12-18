from __future__ import annotations
from collections import defaultdict
from typing import Callable, Dict, List, Any

EventHandler = Callable[[Dict[str, Any]], None]

class EventBus:
    """Simple publish/subscribe event bus.
    Usage:
      bus.subscribe("FOOD_EATEN", handler)
      bus.publish("FOOD_EATEN", {"pos": (x,y)})
    """

    def __init__(self) -> None:
        self._subs: Dict[str, List[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        if handler not in self._subs[event_type]:
            self._subs[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        if handler in self._subs[event_type]:
            self._subs[event_type].remove(handler)
            if not self._subs[event_type]:
                del self._subs[event_type]

    def publish(self, event_type: str, payload: Dict[str, Any] | None = None) -> None:
        handlers = list(self._subs.get(event_type, []))
        for h in handlers:
            try:
                h(payload or {})
            except Exception:
                # Fail-safe: one faulty handler should not break others
                pass

