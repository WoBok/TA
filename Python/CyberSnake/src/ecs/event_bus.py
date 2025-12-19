from __future__ import annotations
from collections import defaultdict
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
import time

EventHandler = Callable[[Dict[str, Any]], None]

@dataclass
class Event:
    type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: Optional[str] = None
    priority: int = 0

class EventBus:
    def __init__(self) -> None:
        self._subscribers: Dict[str, List[EventHandler]] = defaultdict(list)
        self._event_queue: List[Event] = []
        self._processing = False

    def subscribe(self, event_type: str, handler: EventHandler, priority: int = 0) -> None:
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)

    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        if handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
            if not self._subscribers[event_type]:
                del self._subscribers[event_type]

    def publish(self, event_type: str, payload: Dict[str, Any] | None = None, source: Optional[str] = None, priority: int = 0) -> None:
        event = Event(
            type=event_type,
            payload=payload or {},
            source=source,
            priority=priority
        )
        self._event_queue.append(event)

    def publish_immediate(self, event_type: str, payload: Dict[str, Any] | None = None, source: Optional[str] = None) -> None:
        handlers = list(self._subscribers.get(event_type, []))
        event_payload = payload or {}
        for handler in handlers:
            try:
                handler(event_payload)
            except Exception as e:
                print(f"Error in event handler for {event_type}: {e}")

    def process_events(self) -> None:
        if self._processing:
            return
        
        self._processing = True
        self._event_queue.sort(key=lambda e: e.priority, reverse=True)
        
        while self._event_queue:
            event = self._event_queue.pop(0)
            handlers = list(self._subscribers.get(event.type, []))
            
            for handler in handlers:
                try:
                    handler(event.payload)
                except Exception as e:
                    print(f"Error in event handler for {event.type}: {e}")
        
        self._processing = False

    def clear_queue(self) -> None:
        self._event_queue.clear()

    def has_subscribers(self, event_type: str) -> bool:
        return event_type in self._subscribers and len(self._subscribers[event_type]) > 0

    def get_subscriber_count(self, event_type: str) -> int:
        return len(self._subscribers.get(event_type, []))
