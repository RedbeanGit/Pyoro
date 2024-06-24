from pyoro.graphics.layers.layer import Layer

GUI_STACK_LEVEL = 2


class GuiLayer(Layer):
    def __init__(self) -> None:
        super().__init__(GUI_STACK_LEVEL)
