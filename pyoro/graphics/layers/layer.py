import pyglet


class Layer:
    def __init__(self, stack_level: int) -> None:
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.Group(order=stack_level)

    def draw(self) -> None:
        self.batch.draw()
