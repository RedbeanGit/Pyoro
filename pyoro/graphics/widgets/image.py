import pyglet

from pyoro.banks.image_bank import ImageBank
from pyoro.graphics.widgets.anchor import AnchorX, AnchorY, calculate_x, calculate_y
from pyoro.graphics.widgets.widget import Widget


class Image(Widget):
    def __init__(
        self,
        batch: pyglet.graphics.Batch,
        group: pyglet.graphics.Group,
        x: int,
        y: int,
        image_id: str,
        anchor_x: AnchorX = AnchorX.LEFT,
        anchor_y: AnchorY = AnchorY.BOTTOM,
    ):
        super().__init__()

        image_bank = ImageBank.get_instance()

        image = image_bank.get(image_id)
        self._image = pyglet.sprite.Sprite(
            img=image,
            x=calculate_x(anchor_x, x, image.width),
            y=calculate_y(anchor_y, y, image.height),
            batch=batch,
            group=group,
        )
