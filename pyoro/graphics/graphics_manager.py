import typing

from pyoro.exceptions.already_initialized import AlreadyInitializedException
from pyoro.graphics.layers.gui_layers.gui_layer import GuiLayer
from pyoro.graphics.layers.gui_layers.main_menu_gui_layer import MainMenuGuiLayer
from pyoro.graphics.layers.gui_layers.splash_gui_layer import SplashGuiLayer
from pyoro.graphics.layers.layer import Layer
from pyoro.graphics.window import Window


class GraphicsManager:
    _instance: typing.ClassVar[typing.Self | None] = None

    def __init__(self):
        if self._instance is not None:
            raise AlreadyInitializedException(
                f"'{self.__class__.__name__}' already initialized"
            )

        Window()  # force Window initialization

        self.gui_layer: GuiLayer | None = None
        self.entity_layer: Layer | None = None
        self.background_layer: Layer | None = None

    @classmethod
    def get_instance(cls) -> typing.Self:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def set_splash_view(self):
        self.gui_layer = SplashGuiLayer()
        self.gui_layer.draw()

    def set_main_menu_view(self):
        self.gui_layer = MainMenuGuiLayer()
        self.gui_layer.draw()

    def set_game_view(self):
        pass

    def set_settings_menu_view(self):
        pass

    def update(self, deltatime: float):
        window = Window.get_instance()
        window.draw(deltatime)
