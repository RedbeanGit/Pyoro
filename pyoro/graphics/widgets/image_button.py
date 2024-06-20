import pyglet
import typing

from pyoro.banks.image_bank import ImageBank
from pyoro.graphics.widgets.button import Button
from pyoro.graphics.widgets.anchor import AnchorX, AnchorY, calculate_x, calculate_y


class ImageButton(Button):
    def __init__(
        self,
        batch: pyglet.graphics.Batch,
        group: pyglet.graphics.Group,
        x: int,
        y: int,
        callback: typing.Callable[[], None],
        image_id: str,
        pressed_image_id: str,
        hover_image_id: str | None = None,
        anchor_x: AnchorX = AnchorX.LEFT,
        anchor_y: AnchorY = AnchorY.TOP,
    ):
        image_bank = ImageBank.get_instance()
        image = image_bank.get(image_id)
        pressed_image = image_bank.get(pressed_image_id)
        hover_image = (
            image_bank.get(hover_image_id) if hover_image_id is not None else None
        )

        super().__init__(  # type: ignore
            x=calculate_x(anchor_x, x, image.width),
            y=calculate_y(anchor_y, y, image.height),
            pressed=pressed_image,
            depressed=image,
            hover=hover_image,
            batch=batch,
            group=group,
        )

        self._callback = callback

    def on_mouse_release(self, x: int, y: int, buttons: int, modifiers: int):
        self._callback()
        return super().on_mouse_release(x, y, buttons, modifiers)  # type: ignore
