import pyglet

from pyoro.configuration import Configuration
from pyoro.graphics.layers.gui_layers.gui_layer import GuiLayer


class SplashGuiLayer(GuiLayer):
    def __init__(self):
        super().__init__()
        configuration = Configuration.get_instance()

        self.icon: pyglet.image.ImageData = pyglet.image.load("res/images/gui/splash.png")  # type: ignore
        self.text = pyglet.text.Label(
            "Loading...",
            font_size=36,
            x=configuration.window_width // 2,
            y=configuration.window_height // 2 - 100,
            anchor_x="center",
            anchor_y="center",
        )

    def draw(self):
        configuration = Configuration.get_instance()

        self.icon.blit(  # type: ignore
            configuration.window_width // 2 - self.icon.width // 2,  # type: ignore
            configuration.window_height // 2 - self.icon.height // 2,  # type: ignore
        )
        self.text.draw()
