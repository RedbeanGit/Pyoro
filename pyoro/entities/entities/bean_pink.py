import typing

from pyoro.entities.entities.abstract_bean import AbstractBean


class BeanPink(AbstractBean):
    IMAGE_IDS = (
        "bean_pink_left",
        "bean_pink_middle",
        "bean_pink_right",
        "explosion_0",
        "explosion_1",
        "explosion_2",
    )

    def __init__(
        self,
        pos: tuple[float, float],
        spawn_angel_func: typing.Callable[[], None] | None = None,
    ):
        super().__init__(pos)
        self.spawn_angel_func = spawn_angel_func

    def catch(self):
        if self.spawn_angel_func:
            self.spawn_angel_func()
        return super().catch()
