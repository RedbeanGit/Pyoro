import pyglet
import typing

from pyoro.configuration import Configuration
from pyoro.exceptions.already_initialized import AlreadyInitializedException


class Window(pyglet.window.Window):
    _instance: typing.ClassVar[typing.Self | None] = None

    def __init__(self):
        if self._instance is not None:
            raise AlreadyInitializedException(
                f"'{self.__class__.__name__}' already initialized"
            )

        super().__init__(*args, **kwargs)  # type: ignore

        configuration = Configuration.get_instance()
        self.set_minimum_size(configuration.window_width, configuration.window_height)
        self.set_size(configuration.window_width, configuration.window_height)
        self.set_caption("Pyoro")  # type: ignore
        self.set_location(100, 100)  # type: ignore
        self.set_visible(True)  # type: ignore

    @classmethod
    def get_instance(cls) -> typing.Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
