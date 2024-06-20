import time
import typing

from pyoro.events.event import Event
from pyoro.events.event_dispatcher import EventDispatcher
from pyoro.events.event_kind import EventKind


class GameLoop:
    _instance: typing.ClassVar[typing.Self | None] = None

    def __init__(self):
        if self._instance is not None:
            raise Exception("GameLoop already initialized")

    @classmethod
    def get_instance(cls) -> typing.Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def on_tick(self, deltatime: float):
        event_dispatcher = EventDispatcher.get_instance()
        event_dispatcher.push(Event(EventKind.TICK, {"deltatime": deltatime}))

    def run(self):
        last_time = time.time()
        while True:
            new_time = time.time()
            self.on_tick(new_time - last_time)
            last_time = new_time
