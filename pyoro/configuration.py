import typing

from pyoro.exceptions.already_initialized import AlreadyInitializedException

DEFAULT_CONFIG: typing.Final = {
    "window_width": 800,
    "window_height": 450,
    "theme_color": "",
}


class Configuration:
    _instance: typing.ClassVar[typing.Self | None] = None
    __slots__ = ["window_width", "window_height"]

    def __init__(self):
        if self._instance is not None:
            raise AlreadyInitializedException(
                f"'{self.__class__.__name__}' already initialized"
            )

        self.window_width = int(DEFAULT_CONFIG["window_width"])
        self.window_height = int(DEFAULT_CONFIG["window_height"])

    @classmethod
    def get_instance(cls) -> typing.Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def load(self):
        pass

    def save(self):
        pass
