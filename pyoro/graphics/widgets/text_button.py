import pyglet
import typing

from pyoro.banks.image_bank import ImageBank
from pyoro.graphics.widgets.button import Button
from pyoro.graphics.widgets.anchor import AnchorX, AnchorY, calculate_x, calculate_y


class TextButton(Button):
    def __init__(
        self,
        batch: pyglet.graphics.Batch,
        group: pyglet.graphics.Group,
        x: int,
        y: int,
        callback: typing.Callable[[], None],
        text: str,
        anchor_x: AnchorX = AnchorX.LEFT,
        anchor_y: AnchorY = AnchorY.TOP,
    ):
        image_bank = ImageBank.get_instance()
        image = image_bank.get("gui_button_background")
        image_pressed = image_bank.get("gui_button_background_pressed")
        image_hover = image_bank.get("gui_button_background_hover")

        super().__init__(  # type: ignore
            x=calculate_x(anchor_x, x, image.width),
            y=calculate_y(anchor_y, y, image.height),
            pressed=image_pressed,
            depressed=image,
            hover=image_hover,
            batch=batch,
            group=group,
        )

        self._callback = callback

        self._label_group = pyglet.graphics.Group(order=group.order + 1)
        self._label = pyglet.text.Label(
            text,
            font_name="Arial",
            font_size=12,
            x=x + image.width // 2,  # type: ignore
            y=y + image.height // 2,  # type: ignore
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
            batch=batch,
            group=self._label_group,
        )

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int):
        self._callback()
        return super().on_mouse_release(x, y, buttons, modifiers)  # type: ignore
