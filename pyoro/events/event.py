import typing

from pyoro.events.event_kind import EventKind


class Event:
    def __init__(
        self, kind: EventKind, metadata: typing.Mapping[str, typing.Any]
    ) -> None:
        self._kind = kind
        self._metadata = metadata

    def get_kind(self) -> EventKind:
        return self._kind

    def get_metadata(self) -> typing.Mapping[str, typing.Any]:
        return self._metadata
