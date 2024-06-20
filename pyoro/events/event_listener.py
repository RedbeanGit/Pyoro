import typing

from pyoro.events.event_kind import EventKind
from pyoro.events.event import Event


class EventListener:
    def __init__(self, event_kind: EventKind, callback: typing.Callable[[Event], None]):
        self.event_kind = event_kind
        self.callback = callback

    def __call__(self, event: Event):
        if event.get_kind() == self.event_kind:
            self.callback(event)
