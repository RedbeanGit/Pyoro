import typing

from pyoro.events.event_listener import EventListener
from pyoro.events.event import Event
from pyoro.exceptions.already_initialized import AlreadyInitializedException


class EventDispatcher:
    _instance: typing.ClassVar[typing.Self | None] = None

    def __init__(self) -> None:
        if self._instance is not None:
            raise AlreadyInitializedException(
                f"'{self.__class__.__name__}' already initialized"
            )
        self.listeners: list[EventListener] = []
        self.events: list[Event] = []

    @classmethod
    def get_instance(cls) -> typing.Self:
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def dispatch(self) -> None:
        for event in self.events:
            self.notify(event)
        self.events.clear()

    def notify(self, event: Event) -> None:
        for listener in self.listeners:
            listener(event)

    def push(self, event: Event) -> None:
        self.events.append(event)

    def add_listener(self, listener: EventListener) -> None:
        self.listeners.append(listener)

    def remove_listener(self, listener: EventListener) -> None:
        self.listeners.remove(listener)

    def clear(self) -> None:
        self.listeners.clear()
